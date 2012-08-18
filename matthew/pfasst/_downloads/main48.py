'''Solve various advection/diffusion type equations with PyPFASST.'''

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
# config

parser = argparse.ArgumentParser(
    description='solve various advection/diffusion type problems')
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
parser.add_argument('-l',
                    type=int,
                    dest='nlevs',
                    default=0,
                    help='number of levels, or level if serial')
parser.add_argument('-s',
                    type=int,
                    dest='steps',
                    default=0,
                    help='number of steps')
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

dim        = options.dim
iterations = pfasst.options.db.iterations or 12

symbolic_sdc = True

nvar  = (1024, 512, 256)
nodes = (9, 5, 3)
qtype = 'GR'

nlevs = len(nvar)
xrat  = nvar[0] / nvar[1]

nproc = MPI.COMM_WORLD.size - 1

dt    = 0.005

if options.nlevs:
  nlevs = options.nlevs

if nproc == 1:
  serial = True
  nlevs  = 1
else:
  serial = False

if options.steps:
  tend  = dt*nproc*options.steps
else:
  tend  = dt*nproc

steps  = int(math.ceil(tend/dt))
blocks = steps/nproc


###############################################################################
# define various hooks

def create_groups(h5, group):
  grp = h5
  for t in group:
    try:
      grp = grp.create_group(str(t))
    except:
      grp = grp[str(t)]
  return grp


def dump_end(level, state, **kwargs):
  '''Send *yend* to the IO processor.'''

  MPI.COMM_WORLD.Gather(level.qend.flatten(), None)


def echo_error(level, state, **kwargs):
  '''Compute and print error based on exact solution.'''

  if level.feval.burgers:
    return

  y1 = np.zeros(level.feval.nqvar)
  level.feval.exact(state.t0+state.dt, y1)

  err = np.log10(abs(level.qend-y1).max())
  #err = np.log10(abs(level.qSDC[:,-1]-y1).max())

  print 'step: %03d, iteration: %03d, position: %d, level: %02d, error: %f' % (
    state.step, state.iteration, state.cycle, level.level, err)


###############################################################################
# pfasst!

world = MPI.COMM_WORLD
i_am_a_worker = world.Get_rank() > 0
worker_comm   = world.Create(world.Get_group().Excl([0]))

if i_am_a_worker:

  root = worker_comm.rank == 0

  pf = pfasst.PFASST()
  pf.simple_communicators(ntime=nproc, comm=worker_comm)

  # add levels
  level = 0
  if serial:
    level = options.nlevs

  F   = AD(nvar[level], dim=dim, burgers=options.burgers)
  sdc = pfasst.imex.IMEXSDC(qtype, nodes[level],
                            symbolic=symbolic_sdc)

  pf.add_level(F, sdc, interpolate, restrict)

  for k in range(level+1, level+nlevs):
    G   = AD(nvar[k], dim=dim, burgers=options.burgers)
    sdc = pfasst.imex.IMEXSDC(qtype, nodes[level],
                              refine=(nodes[level]-1)/(nodes[k]-1),
                              symbolic=symbolic_sdc)
    pf.add_level(G, sdc, interpolate, restrict)

  if not serial:
    for l in range(1, nlevs):
      pf.levels[l].sweeps = l+1


  # add hooks
  if options.output:
    pf.add_hook(0, 'post-sweep', dump_end)

  else:
    if not pfasst.options.db.verbose_cycle:
      pf.add_hook(0, 'post-sweep', echo_error)
      for k in range(1, nlevs):
        pf.add_hook(k, 'post-sweep', echo_error)

  if options.timing:
    pfasst.options.db.timing = True

  # receive initial condition and run
  u0 = np.zeros(nvar[level]**dim, dtype=np.float64)
  world.Bcast(u0)

  pf.run(u0, dt, tend, iterations,
         dim=dim, xrat=xrat, interpolation_order=-1)

  # dump timings
  if options.timing:
    timings = pf.timer.gather_timings(comm=worker_comm)
    if worker_comm.rank == 0:
      np.save(options.timing, timings)


else: # i am the io processor

  # load and send initial condition
  level = 0
  if serial:
    level = options.nlevs
  u0 = np.zeros(nvar[level]**dim, dtype=np.float64)

  if options.initial:
    import h5py
    import os

    h5 = h5py.File(options.initial, 'r')
    h5['u0'].read_direct(u0)
    h5.close()
  else:

    F = AD(nvar[level], dim=dim)
    F.exact(0.0, u0)

  world.Bcast(u0)

  # gather output
  if options.output:
    import h5py

    h5   = h5py.File(options.output, 'w')
    fgrp = h5.create_group('solutions')
    fgrp = fgrp.create_group('levels')

    # gather data from workers
    u1   = np.zeros((nproc+1, nvar[level]**dim))
    fset = fgrp.create_dataset('0',
                               (steps, iterations, nvar[level]**dim),
                               dtype=np.float64)

    for n in range(blocks):
      for i in range(iterations):
        world.Gather(u0, u1)
        fset[n*nproc:(n+1)*nproc,i,:] = u1[1:,:]

    h5.close()
