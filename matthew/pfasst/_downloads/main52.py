'''Solve the KS equation with PFASST.'''

# Copyright (c) 2011, Matthew Emmett.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


from mpi4py import MPI

import argparse
import math

import h5py

import numpy as np
import numpy.fft as fft

import pfasst
import pfasst.imex
import pfasst.options

from ks import *


######################################################################
# options

parser = argparse.ArgumentParser(
    description='solve the KS equation')
parser.add_argument('-s',
                    type=int,
                    dest='steps',
                    default=0,
                    help='number of steps')
parser.add_argument('-i',
                    type=str,
                    dest='initial',
                    default='',
                    help='input file')
parser.add_argument('-o',
                    type=str,
                    dest='output',
                    default='',
                    help='output file')
parser.add_argument('-a',
                    dest='dump_iterations',
                    default=False,
                    action='store_true',
                    help='dump iterations?')
# parser.add_argument('-b',
#                     dest='dump_blocked',
#                     default=False,
#                     action='store_true',
#                     help='dump only at the end of each block?')
parser.add_argument('-p',
                    dest='profile',
                    default=False,
                    action='store_true',
                    help='profile?')
parser.add_argument('-t',
                    type=str,
                    dest='timing',
                    default='',
                    help='timing output file')
remaining_args = pfasst.options.parse_known_args()
options = parser.parse_args(remaining_args)


######################################################################
# load initial condition

try:
  h5 = h5py.File(options.initial, 'r')
except:
  print 'Unable to open initial condition.'
  raise SystemExit

u0 = np.zeros(h5['u0'].shape, dtype=h5['u0'].dtype)
h5['u0'].read_direct(u0)
h5.close()

######################################################################
# config

shape = u0.shape
nvar  = (u0.shape[0], u0.shape[0]/2)
dt    = 4.0/nvar[0]

dim = 2
nodes = (5, 3)
qtype = 'GL'

comm  = MPI.COMM_WORLD
nproc = comm.size
if options.steps:
  tend = dt*nproc*options.steps
else:
  tend = dt*nproc

steps  = int(math.ceil(tend/dt))
blocks = steps/nproc
if nproc > 1:
  iterations = pfasst.options.db.iterations or 6
else:
  iterations = pfasst.options.db.iterations or 10


######################################################################
# init pfasst

pf = pfasst.PFASST()
pf.simple_communicators(ntime=nproc, comm=comm)

# add levels
F   = KS(nvar[0])
sdc = pfasst.imex.IMEXSDC('GL', nodes[0])
pf.add_level(F, sdc, interpolate, restrict)

for l in range(1, len(nvar)):
  G   = KS(nvar[1])
  sdc = pfasst.imex.IMEXSDC('GL', nodes[0],
                            refine=(nodes[0]-1)/(nodes[1]-1))
  pf.add_level(G, sdc)

pf.levels[1].sweeps = 2

# output
def dump(level, state, **kwargs):
  import lockfile

  lock = lockfile.FileLock(options.output)
  with lock:

    h5   = h5py.File(options.output, 'a')
    dset = h5['/solutions/levels/0']

    qend = np.real(fft.ifftn(np.reshape(level.qend[:], dim*(nvar[0],)))).flatten()

    if options.dump_iterations:
      dset[state.step,state.iteration,:] = qend
    else:
      dset[state.step,:] = qend

    h5.close()


if options.output:

  h5   = h5py.File(options.output, 'w')
  fgrp = h5.create_group('solutions')
  fgrp = fgrp.create_group('levels')

  #dump_steps = steps if not options.dump_blocked else blocks
  dump_steps = steps
  dump_nvar  = nvar[0]**dim

  if options.dump_iterations:
    dump_shape = [dump_steps, iterations, dump_nvar]
    pf.add_hook(0, 'post-sweep', dump)
  else:
    dump_shape = [dump_steps, dump_nvar]
    pf.add_hook(0, 'end-step', dump)

  fgrp.create_dataset('0', tuple(dump_shape), dtype=np.float64)

  h5.close()


######################################################################
# run

if comm.rank == 0:
  print 'kuramoto_silvashinsky:'
  print '  pfasst:'
  print '    nproc:', nproc
  print '    iterations:', iterations
  print '  initial:', options.initial
  print '  output:'
  print '    output:', options.output
  print '    iterations:', options.dump_iterations
  #print '    blocked:', options.dump_blocked
  print '  parameters:'
  print '    dt:', dt
  print '    tend:', tend
  print '    steps:', steps
  print '    shape: [', ', '.join(map(str, shape)), ']'
  #print '  dumps:'

if options.profile:
  import cProfile
  cProfile.run('pf.run(u0, dt, tend, iterations)', 'pfprof_%d' % pf.mpi.rank)
else:
  pf.run(fft.fftn(u0).flatten(), dt, tend, iterations)

# save timing info

if comm.rank == 0:
  if options.timing:
    timings = pf.timer.gather_timings(comm=comm)
    np.save(options.timing, timings)

  if options.profile:
    import pstats
    p = pstats.Stats('pfprof_%d' % pf.mpi.rank)
    p.strip_dirs().sort_stats('time').print_stats(20)

else:
  if options.timing:
    pf.timer.gather_timings(comm=comm)
