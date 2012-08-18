'''SW FEval class.'''

import numpy as np

import pfasst.explicit
import reconstruct

class SW2D(pfasst.explicit.ExplicitFEval):
  '''Explicit function evaluation class for the 2d shallow-water equations.

  :param N: 2-tuple of grid size.

  :attribute q_r: reconstructed q values

  Note that *q_r* is indexed as:

  >>> q_r[i,j,c,k,p,n]

  where

  * *i* and *j* index the cell,
  * *c* indexes the component (0=height, 1=momentum),
  * *k* indexes the quadrature point (0, 1, or 2),
  * *p* indexes the plus/minus limit direction (0=minus, 1=plus), and
  * *n* indexes the nodal direction (0=x-nodal, 1=y-nodal),

  '''

  def __init__(self, N, L):

    Nc = 3                              # number of components
    Ng = 4                              # number of ghost cells

    # allocate work space
    Nx, Ny = N

    # init reconstructor
    self.reconstructor = reconstruct.Reconstruct((Nx+2*Ng,Ny+2*Ng))

    # save
    self.N     = N
    self.shape = (Nx, Ny, Nc)
    self.nqvar = Nx*Ny*Nc
    self.nfvar = Nx*Ny*Nc
    self.Nc    = Nc
    self.Ng    = Ng
    self.dx    = np.array(L) / np.array(N)
    self.weights = np.array([5.0/9.0, 8.0/9.0, 5.0/9.0])


  def evaluate(self, y, t, out, **kwargs):
    r'''Evaluate function values *f(y, t)*.

    :param y: y (numpy array)
    :param t: time (float)
    :param f: result (numpy array)

    The (flattened) result is stored in *f*.
    '''

    shape  = self.shape
    Nc     = self.Nc
    Ng     = self.Ng
    w      = self.weights
    Nx, Ny = self.N
    dx, dy = self.dx

    Nq = 3

    h      = 0
    uh     = 1
    vh     = 2
    xnodal = 0
    ynodal = 1
    minus  = 0
    plus   = 1
    
    #### init ghost cells
    q  = np.reshape(y, shape)
    qg = np.zeros((Nx+2*Ng,Ny+2*Ng,Nc))

    qg[ Ng:-Ng, Ng:-Ng, :] = q[   :  ,   :  , :]
    qg[   :Ng , Ng:-Ng, :] = q[-Ng:  ,   :  , :]
    qg[-Ng:   , Ng:-Ng, :] = q[   :Ng,   :  , :]    
    qg[Ng:-Ng,    :Ng , :] = q[   :  ,-Ng:  , :]
    qg[Ng:-Ng, -Ng:   , :] = q[   :  ,   :Ng, :]

    qr = np.zeros((Nx+2*Ng,Ny+2*Ng,Nc,Nq,2,2))

    #### reconstruct
    for c in range(Nc):
      self.reconstructor.reconstruct_boundary(qg[:,:,c],
                                              qr[:,:,c,:,:,xnodal],
                                              qr[:,:,c,:,:,ynodal])

    #### compute plus/minus fluxes
    f  = np.zeros((Nx+1,Ny+1,Nc,Nq,2,2))   # same indexing as qr
    qr = qr[Ng:-Ng+1,Ng:-Ng+1,:,:,:,:]     # extract non-ghost cells

    assert(f.shape == qr.shape)

    # height
    f[:,:,h,:,:,xnodal] = qr[:,:,uh,:,:,xnodal]
    f[:,:,h,:,:,ynodal] = qr[:,:,vh,:,:,ynodal]    

    # x-momentum
    f[:,:,uh,:,:,xnodal] = ( np.square(qr[:,:,uh,:,:,xnodal]) / qr[:,:,h,:,:,xnodal]
                             + 0.5*np.square(qr[:,:,h,:,:,xnodal]) )
    f[:,:,uh,:,:,ynodal] = ( qr[:,:,uh,:,:,ynodal] * qr[:,:,vh,:,:,ynodal]
                             / qr[:,:,h,:,:,ynodal] )

    # y-momentum
    f[:,:,vh,:,:,xnodal] = ( qr[:,:,uh,:,:,xnodal] * qr[:,:,vh,:,:,xnodal]
                             / qr[:,:,h,:,:,xnodal] )
    f[:,:,vh,:,:,ynodal] = ( np.square(qr[:,:,vh,:,:,ynodal]) / qr[:,:,h,:,:,ynodal]
                             + 0.5*np.square(qr[:,:,h,:,:,ynodal]) )

    #### compute LF fluxes
    alpha = 2.0
    flux = np.zeros((Nx+1,Ny+1,Nc,Nq,2))
    flux[:,:,:,:,:] = 0.5*( f[:,:,:,:,minus,:] + f[:,:,:,:,plus,:] -
                            alpha * ( qr[:,:,:,:,plus,:] - qr[:,:,:,:,minus,:] ) )

    #### compute net fluxes
    net = np.zeros((Nx,Ny,Nc))
    net[:,:,:] += - ( np.dot(flux[1:,:-1,:,:,xnodal], w)
                      - np.dot(flux[:-1,:-1,:,:,xnodal], w) ) / dx
    net[:,:,:] += - ( np.dot(flux[:-1,1:,:,:,ynodal], w)
                      - np.dot(flux[:-1,:-1,:,:,ynodal], w) ) / dy

    # done
    out[:] = net.flatten()

