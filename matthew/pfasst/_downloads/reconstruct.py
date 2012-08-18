'''Finite-volume WENO reconstructor.

   Note that: - q_x denotes...
              - q_y denotes...

'''

import math

import numpy as np

from sw.creconstruct import *


###############################################################################

def reconstruction_points(N, domain=[(0.0,0.0), (1.0,1.0)]):

    d = np.array(domain)
    N = np.array(N)
    L = d[1,:] - d[0,:]

    Nx, Ny = N
    dx, dy = L / N
    x0, y0 = d[0,:]

    x_x = np.zeros((Nx+1, Ny+1, 3, 2))
    x_y = np.zeros((Nx+1, Ny+1, 3, 2))
    y_x = np.zeros((Nx+1, Ny+1, 3, 2))
    y_y = np.zeros((Nx+1, Ny+1, 3, 2))

    for i in range(Nx+1):
      xm = x0 + (i+0)*dx

      x_x[i,:,:,:] = xm

      x_y[i,:,0,:] = xm + 0.5*dx*(1.0 - math.sqrt(3.0/5.0))
      x_y[i,:,1,:] = xm + 0.5*dx
      x_y[i,:,2,:] = xm + 0.5*dx*(1.0 + math.sqrt(3.0/5.0))

    for j in range(Ny+1):
      ym = y0 + (j+0)*dy

      y_y[:,j,:,:] = ym

      y_x[:,j,0,:] = ym + 0.5*dy*(1.0 - math.sqrt(3.0/5.0))
      y_x[:,j,1,:] = ym + 0.5*dy
      y_x[:,j,2,:] = ym + 0.5*dy*(1.0 + math.sqrt(3.0/5.0))

    return x_x, y_x, x_y, y_y


###############################################################################

class Reconstruct(object):
  '''Finite-volume WENO reconstruction (2d).

  :param N: 2-tuple of grid size.
  '''

  k = 3                                 # WENO order 2k-1


  def __init__(self, N):

    self.N = N


  def reconstruct_boundary(self, q, qr_x, qr_y):
    '''Reconstruct *q* and store the results in *qr_x* and *qr_y*.

    :param q: cell averaged quantities
    :param qr_x: x-nodal result
    :param qr_y: y-nodal result

    The *qr_x* and *qr_y* result arrays are indexed according to, eg::

    >>> qr_x[i,j,k,p]

    where:

    * *i* and *j* index the cell,
    * *k* indexes the quadrature point (0, 1, or 2), and
    * *p* indexes the plus/minus limit direction (0 for minus, 1 for
       plus).

    '''

    Nx, Ny = self.N
    k      = self.k
    Nq     = 3

    #### allocate

    # i, j: x and y indexes
    # l: quadrature point index
    # r: left shift index
    # s: split-weight index

    sigma_h = np.zeros((Nx,k))               # horiz slice: i, r
    sigma_v = np.zeros((Ny,k))               # vert slice:  j, r

    omega_h      = np.zeros((Ny,Nq,Nx,k))    # horiz slice: j, l, i, r
    omega_v      = np.zeros((Nx,Nq,Ny,k))    # vert slice:  i, l, j, r
    omega_quad_h = np.zeros((Ny,Nx,Nq,k,2))  # horiz slice: j, i, l, r, s
    omega_quad_v = np.zeros((Nx,Ny,Nq,k,2))  # vert slice:  i, j, l, r, s

    qr_quad_h = np.zeros((Ny,Nx,Nq))         # horiz recon: j, i, l
    qr_quad_v = np.zeros((Nx,Ny,Nq))         # vert recon:  i, j, l

    #### x-nodal

    for i in xrange(Nx):
      smoothness(q[i,:], sigma_v)
      weights_quad(sigma_v, omega_quad_v[i,:,:,:,:])
      reconstruct_quad(q[i,:], omega_quad_v[i,:,:,:,:], qr_quad_v[i,:,:])

    for j in xrange(Ny):
      for l in xrange(Nq):
        smoothness(qr_quad_v[:,j,l], sigma_h)

        weights_left(sigma_h, omega_h[j,l,:,:])
        reconstruct_left(qr_quad_v[:,j,l], omega_h[j,l,:,:], qr_x[:,j,l,1])

        weights_right(sigma_h, omega_h[j,l,:,:])
        reconstruct_right(qr_quad_v[:,j,l], omega_h[j,l,:,:], qr_x[1:,j,l,0])


    #### y-nodal

    for j in xrange(Ny):
      smoothness(q[:,j], sigma_h)
      weights_quad(sigma_h, omega_quad_h[j,:,:,:,:])
      reconstruct_quad(q[:,j], omega_quad_h[j,:,:,:,:], qr_quad_h[j,:,:])

    for i in xrange(Nx):
      for l in xrange(Nq):
        smoothness(qr_quad_h[:,i,l], sigma_v)
        
        weights_left(sigma_v, omega_v[i,l,:,:])
        reconstruct_left(qr_quad_h[:,i,l], omega_v[i,l,:,:], qr_y[i,:,l,1])
        
        weights_right(sigma_v, omega_v[i,l,:,:])
        reconstruct_right(qr_quad_h[:,i,l], omega_v[i,l,:,:], qr_y[i,1:,l,0])


  def reconstruct_volume(self, q, qr):
    '''Reconstruct *q* at the internal quadrature points (for interpolation).

    :param q:  cell averaged quantities
    :param qr: result

    The result array is indexed according to::

    >>> qr[i,j,ki,kj]

    where:

    * *i* and *j* index the cell, and
    * *k* indexes the quadrature point (0, 1, 2, 3, 4, or 5).

    '''

    Nx, Ny = self.N
    k      = self.k
    Nq     = 6

    #### allocate

    # i, j: x and y indexes
    # l: quadrature point index
    # r: left shift index
    # s: split-weight index

    sigma_v = np.zeros((Ny,k))            # vert slices:  j, r
    sigma_h = np.zeros((Nx,k))            # horiz slices: i, r

    omega_v = np.zeros((Nx,Ny,Nq,k,2))    # vert slices:  i, j, l, r, s
    omega_h = np.zeros((Ny,Nq,Nx,Nq,k,2)) # horiz slices: j, lj, i, li, r, s

    qr_v    = np.zeros((Nx,Ny,Nq))        # vert recon:   i, j, l

    #### volume

    for i in xrange(Nx):
      smoothness(q[i,:], sigma_v)
      weights_interp(sigma_v, omega_v[i,:,:,:,:])
      reconstruct_interp(q[i,:], omega_v[i,:,:,:,:], qr_v[i,:,:])

    for j in xrange(Ny):
      for l in xrange(Nq):
        smoothness(qr_v[:,j,l], sigma_h)

        weights_interp(sigma_h, omega_h[j,l,:,:,:,:])
        reconstruct_interp(qr_v[:,j,l], omega_h[j,l,:,:,:,:], qr[:,j,:,l])
