"""Solve various advection/diffusion type equations with PyPFASST."""

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

import numpy as np
import numpy.fft as fft

import pfasst
import pfasst.imex
import pfasst.options

from pfasst.interpolators import spectral_periodic_masks

from ad import *

###############################################################################
# options

parser = argparse.ArgumentParser(
    description='solve various advection/diffusion type problems')
parser.add_argument('-i',
                    type=str,
                    dest='initial',
                    default='',
                    help='initial condition')
parser.add_argument('-o',
                    type=str,
                    dest='output',
                    default='',
                    help='output file')
parser.add_argument('-d',
                    type=int,
                    dest='dim',
                    default=1,
                    help='number of dimensions')
parser.add_argument('-b',
                    dest='burgers',
                    default=False,
                    action='store_true',
                    help="solve the viscous Burger's eqn")
parser.add_argument('-q',
                    type=str,
                    dest='qtype',
                    default='GL',
                    help="quadrature type")
parser.add_argument('-l',
                    type=int,
                    dest='nlevs',
                    default=0,
                    help='number of levels, or level if serial')
parser.add_argument('-r',
                    type=int,
                    dest='refine',
                    default=1,
                    help='time step refinement')
parser.add_argument('-s',
                    type=int,
                    dest='steps',
                    default=0,
                    help='number of steps')
parser.add_argument('-f',
                    type=float,
                    dest='tend',
                    default=1.0,
                    help='final (end) time')
parser.add_argument('-n',
                    type=float,
                    dest='nu',
                    default=0.005,
                    help='nu')
parser.add_argument('-v',
                    dest='verbose',
                    default=False,
                    action='store_true',
                    help='echo verbose cycle progression?')
parser.add_argument('-t',
                    type=str,
                    dest='timing',
                    default='',
                    help='timing output file')

remaining_args = pfasst.options.parse_known_args()
options        = parser.parse_args(remaining_args)

nproc  = MPI.COMM_WORLD.size
serial = nproc == 1

# levels
if serial:
  nlevs = 1
  level = options.nlevs
elif options.nlevs:
  nlevs = options.nlevs
  level = 0
else:
  nlevs = 3
  level = 0

# time
iterations   = pfasst.options.db.iterations or 12
symbolic_sdc = True
nodes        = [9, 5, 3][level:level+nlevs]
#nodes        = [5, 3, 2][level:level+nlevs]

if options.refine > 1:
  nodes = [ 5 ]

tend = options.tend

if options.steps:
  dt = tend / options.steps / options.refine
else:
  dt = tend / nproc / options.refine

steps  = int(math.ceil(tend/dt))
blocks = steps/nproc


###############################################################################
# load initial condition

if options.initial:
  import h5py

  h5 = h5py.File(options.initial, 'r')
  u0 = np.zeros(h5['u0'].shape, dtype=h5['u0'].dtype)
  h5['u0'].read_direct(u0)
  h5.close()

else:
  u0 = np.zeros(1024**options.dim, dtype=np.float64)
  F = AD(1024, dim=options.dim)
  F.exact(0.0, u0)

nvar = []
for level in range(nlevs):
  nvar.append(u0.shape[0]/2**level)


###############################################################################
# hooks

def dump(level, state, **kwargs):
  """Dump solution."""

  if (state.step+1) % options.refine != 0:
    return

  step = (state.step+1)/options.refine-1

  lock = lockfile.FileLock(options.output)
  with lock:
    h5   = h5py.File(options.output, 'a')
    dset = h5['/solutions/levels/0']
    dset[step,state.iteration,:] = level.qend
    h5.close()


def echo_error(level, state, **kwargs):
  """Compute and print error based on exact solution."""

  if level.feval.burgers:
    return

  y1 = np.zeros(level.feval.nqvar)
  level.feval.exact(state.t0+state.dt, y1)

  err = np.log10(abs(level.qend-y1).max())

  print 'step: %03d, iteration: %03d, position: %d, level: %02d, error: %f' % (
    state.step, state.iteration, state.cycle, level.level, err)


###############################################################################
# init pfasst

pf = pfasst.PFASST()
pf.simple_communicators(ntime=nproc)

# add levels
F   = AD(nvar[0], dim=options.dim, burgers=options.burgers, nu=options.nu)
sdc = pfasst.imex.IMEXSDC(options.qtype, nodes[0],
                          symbolic=symbolic_sdc)
pf.add_level(F, sdc, interpolate, restrict)

for k in range(1, nlevs):
  G   = AD(nvar[k], dim=options.dim, burgers=options.burgers, nu=options.nu)
  sdc = pfasst.imex.IMEXSDC(options.qtype, nodes[0],
                            refine=(nodes[0]-1)/(nodes[k]-1),
                            symbolic=symbolic_sdc)
  pf.add_level(G, sdc, interpolate, restrict)


# if nlevs > 1:
#   #pf.levels[1].sweeps = 2
#   pf.levels[-1].sweeps = 2

# def inc_sweeps(level, state, **kwargs):
#   level.sweeps = 2

#pf.add_hook(nlevs-1, 'post-predictor', inc_sweeps)

# init output
if options.output:
  import h5py
  import lockfile

  shape = (steps/options.refine, iterations, nvar[0]**options.dim)

  if MPI.COMM_WORLD.rank == 0:
    lock = lockfile.FileLock(options.output)
    with lock:
      h5   = h5py.File(options.output, 'w')
      fgrp = h5.create_group('solutions')
      fgrp = fgrp.create_group('levels')
      fgrp.create_dataset('0', shape, dtype=u0.dtype)
      h5.close()

  pf.add_hook(0, 'post-sweep', dump)

else:
  if not pfasst.options.db.verbose_cycle:
    pf.add_hook(0, 'post-sweep', echo_error)
    for k in range(1, nlevs):
      pf.add_hook(k, 'post-sweep', echo_error)


###############################################################################
# run

if options.timing:
  pfasst.options.db.timing = True

pf.run(u0, dt, tend, iterations, dim=options.dim, interpolation_order=-1)

# dump timings
if options.timing:
  timings = pf.timer.gather_timings(comm=worker_comm)
  if worker_comm.rank == 0:
    np.save(options.timing, timings)
