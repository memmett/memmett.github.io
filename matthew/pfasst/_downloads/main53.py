"""PFASST 2d shallow-water solver."""

from mpi4py import MPI

import argparse
import math

import numpy as np
import h5py

import pfasst
import pfasst.explicit
import pfasst.options

import sw

###############################################################################
# config

parser = argparse.ArgumentParser()
parser.add_argument('-n',
                    type=int,
                    dest='nspace',
                    default=1,
                    help='number of spatial processors')
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
parser.add_argument('-o',
                    type=str,
                    dest='output',
                    default='',
                    help='output file')
parser.add_argument(type=str,
                    dest='initial',
                    help='input file')
remaining_args = pfasst.options.parse_known_args()
options = parser.parse_args(remaining_args)

dim   = 2
nodes = (5, 3)

nspace     = options.nspace
ntime      = (MPI.COMM_WORLD.size - 1)/nspace
dt         = 0.5/128
tend       = dt*ntime
steps      = int(math.ceil(tend/dt))
iterations = pfasst.options.db.iterations or 4
blocks     = steps/ntime


###############################################################################
# hooks

def gather_yend(level, state, **kwargs):
  '''Send *yend* to the IO processor.'''

  MPI.COMM_WORLD.Gather(level.qend.flatten(), None)


###############################################################################
# pfasst!

world = MPI.COMM_WORLD
worker_comm   = world.Create(world.Get_group().Excl([0]))

if world.rank > 0:

  # init pfasst
  pf = pfasst.PFASST()
  pf.simple_communicators(ntime=ntime,
                          nspace=nspace,
                          comm=worker_comm)

  # receive shape and initial condition from io processor
  shape = np.zeros(dim+1, dtype=np.int)
  world.Bcast(shape)

  u0 = np.zeros(shape).flatten()
  world.Bcast(u0)

  # add fine level
  N   = shape[:2]
  F   = sw.SW2D(N, dim*(1.0,), pf.mpi.space, nspace>1)
  sdc = pfasst.explicit.ExplicitSDC('GL', nodes[0])
  pf.add_level(F, sdc, sw.interpolate, sw.restrict)

  # add coarse level
  if ntime > 1:
    G   = sw.SW2D(N/2, dim*(1.0,), pf.mpi.space, nspace>1)
    sdc = pfasst.explicit.ExplicitSDC('GL', nodes[1])
    pf.add_level(G, sdc)

  # send ranks and ranges to io processor
  ranges = np.zeros(4, dtype=np.int)
  ranges[0], ranges[1] = F.ranges[0]
  ranges[2], ranges[3] = F.ranges[1]
  world.Gather(ranges, None)

  ranks = np.zeros(2, dtype=np.int)
  ranks[0] = pf.mpi.rank
  ranks[1] = pf.mpi.space.rank
  world.Gather(ranks, None)

  # trim initial condition according to ranges
  u0 = np.reshape(u0, shape)
  u0 = u0[ranges[0]:ranges[1],ranges[2]:ranges[3]].flatten()

  # run!
  if options.output:
    pf.add_hook(0, 'post-sweep', gather_yend)

  if options.profile:
    import cProfile
    cProfile.run('pf.run(u0, dt, tend, iterations)', 'pfprof_%d' % pf.mpi.rank)
  else:
    pf.run(u0, dt, tend, iterations)

  if worker_comm.rank == 0:
    if options.timing:
      timings = pf.timer.gather_timings(comm=worker_comm)
      np.save(options.timing, timings)

    if options.profile:
      import pstats
      p = pstats.Stats('pfprof_%d' % pf.mpi.rank)
      p.strip_dirs().sort_stats('time').print_stats(20)

  else:
    if options.timing:
      pf.timer.gather_timings(comm=worker_comm)


else:                           # io processor

  # load and send initial condition
  h5   = h5py.File(options.initial, 'r')
  dset = h5['u0']
  u0   = np.zeros(dset.shape)
  dset.read_direct(u0)
  h5.close()

  # broadcase shape and initial condition
  shape = np.array(list(u0.shape), dtype=np.int)
  world.Bcast(shape)
  world.Bcast(u0.flatten())

  # gather ranges from workers
  ranges = np.zeros((ntime*nspace+1, 4), dtype=np.int)
  world.Gather(np.zeros(4, dtype=np.int), ranges)
  ranges = ranges[1:,:]

  ranks = np.zeros((ntime*nspace+1, 2), dtype=np.int)
  world.Gather(np.zeros(2, dtype=np.int), ranks)
  ranks = ranks[1:,:]

  print 'shallow_water:'
  print '  pfasst:'
  print '    ntime:', ntime
  print '    nspace:', nspace
  print '    iterations:', iterations
  print '  parameters:'
  print '    dt:', dt
  print '    tend:', tend
  print '    steps:', steps
  print '    shape:', tuple(shape)
  print '  output: %s' % options.output
  print '  dumps:'

  # open and init output file
  if options.output:

    h5   = h5py.File(options.output, 'w')
    fgrp = h5.create_group('solutions')
    fgrp = fgrp.create_group('0')
    fgrp.create_dataset('shape', data=shape)

    # create receive space and dataset
    nvar = np.prod(shape)
    u1   = np.zeros((ntime*nspace+1, nvar/nspace))
    fshape = (steps, iterations,) + tuple(shape)
    fset   = fgrp.create_dataset('q', fshape, dtype=np.float64)

    # gather iterations (from the 'gather_yend' hook above)
    u2 = np.zeros(nvar/nspace)
    for n in range(blocks):
      print '    - block:', n
      for i in range(iterations):
        print '      - iteration:', i
        world.Gather(u2, u1)

        for wrank, (trank, srank) in enumerate(ranks):
          x0, x1, y0, y1 = ranges[wrank]
          q = np.reshape(u1[wrank+1,:], (x1-x0, y1-y0, shape[2]))
          fset[n*ntime+trank,i,x0:x1,y0:y1,:] = q[:,:,:]

    # done
    h5.close()

