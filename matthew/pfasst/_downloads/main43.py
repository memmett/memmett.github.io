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
parser.add_argument('-b',
                    dest='dump_blocked',
                    default=False,
                    action='store_true',
                    help='dump only at the end of each block?')
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
# config

world  = MPI.COMM_WORLD
worker = world.rank > 0
worker_comm = world.Create(world.Get_group().Excl([0]))

dim = 2
nodes = (5, 3)
qtype = 'GL'
nproc = world.size - 1

# send/receive shape
if worker:

  shape = np.zeros(dim, dtype=int)

else:

  if options.initial:
    h5 = h5py.File(options.initial, 'r')
    shape = np.array(h5['u0'].shape, dtype=int)
    h5.close()
  else:
    shape = np.array([512, 512], dtype=int)

world.Bcast(shape)

nvar = (shape[0], shape[0]/2)
dt   = 4.0/nvar[0]

if options.steps:
  tend  = dt*nproc*options.steps
else:
  tend  = dt*nproc

steps      = int(math.ceil(tend/dt))
blocks     = steps/nproc
if nproc > 1:
  iterations = pfasst.options.db.iterations or 6
else:
  iterations = pfasst.options.db.iterations or 10

######################################################################
# main

def gather_yend(yend=None, iteration=None, **kwargs):

  MPI.COMM_WORLD.Gather(yend.flatten(), None)


if worker:

  pf = pfasst.pfasst.PFASST()
  pf.simple_communicators(ntime=nproc, comm=worker_comm)

  # add levels
  F   = KS(nvar[0])
  sdc = pfasst.imex.IMEXSDC('GL', nodes[0])
  pf.add_level(F, sdc, interpolate, restrict)

  G   = KS(nvar[1])
  sdc = pfasst.imex.IMEXSDC('GL', nodes[0],
                            refine=(nodes[0]-1)/(nodes[1]-1))
  pf.add_level(G, sdc)
  pf.simple_sweeps[1] = 2

  # receive initial condition
  u0 = np.zeros(nvar[0]**dim, dtype=np.complex128)
  world.Bcast(u0)

  # run!
  if options.output:
    if options.dump_iterations:
      pf.add_hook(0, 'sweep', gather_yend)
    else:
      pf.add_hook(0, 'end', gather_yend)

  if options.profile:
    import cProfile
    cProfile.run('pf.run(u0, dt, tend, iterations)', 'pfprof_%d' % pf.rank)
  else:
    pf.run(u0, dt, tend, iterations)

  if worker_comm.rank == 0:
    if options.timing:
      timings = pf.timer.gather_timings(comm=worker_comm)
      np.save(options.timing, timings)

    if options.profile:
      import pstats
      p = pstats.Stats('pfprof_%d' % pf.rank)
      p.strip_dirs().sort_stats('time').print_stats(20)

  else:
    if options.timing:
      pf.timer.gather_timings(comm=worker_comm)


else: # io processor
  
  if options.initial:
    h5   = h5py.File(options.initial, 'r')
    dset = h5['u0']

    u0 = np.zeros(shape, dtype=np.float64)
    dset.read_direct(u0)

    z0 = fft.fftn(u0).flatten()
    world.Bcast(z0)

    h5.close()

  else:
    raise ValueError, 'initial condition must be specified (eg, -i ks_initial.h5)'

  print 'kuramoto_silvashinsky:'
  print '  pfasst:'
  print '    nproc:', nproc
  print '    iterations:', iterations
  print '  initial:', options.initial
  print '  output:'
  print '    output:', options.output
  print '    iterations:', options.dump_iterations
  print '    blocked:', options.dump_blocked
  print '  parameters:'
  print '    dt:', dt
  print '    tend:', tend
  print '    steps:', steps
  print '    shape: [', ', '.join(map(str, shape)), ']'
  print '  dumps:'

  if options.output:

    h5   = h5py.File(options.output, 'w')
    fgrp = h5.create_group('solutions')
    fgrp = fgrp.create_group('levels')
    u1   = np.zeros((nproc+1, nvar[0]**dim), dtype=np.complex128)

    dump_steps = steps if not options.dump_blocked else blocks
    dump_nvar  = nvar[0]**dim
    dump_shape = [dump_steps, iterations, dump_nvar]

    if not options.dump_iterations:
      del dump_shape[1]

    fset = fgrp.create_dataset('0',
               tuple(dump_shape), dtype=np.float64)

    iters = range(iterations) if options.dump_iterations else [ iterations-1 ]
    procs = range(nproc) if not options.dump_blocked else [ nproc-1 ]

    for n in range(blocks):
      for i in iters:
        world.Gather(u0, u1)
        for p in procs:
          print '    - step: %9d, iteration: %3d' % (n*nproc+p, i)

          q = np.real(fft.ifftn(np.reshape(u1[p+1,:], dim*(nvar[0],)))).flatten()
          
          s = n*nproc+p if not options.dump_blocked else n

          if options.dump_iterations:
            fset[s,i,:] = q
          else:
            fset[s,:] = q

    # done
    h5.close()
