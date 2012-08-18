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


import math

import numpy as np
import numpy.fft as fft

import pfasst.imex

from pfasst.interpolators import spectral_periodic_masks


######################################################################
# KS FEval

class KS(pfasst.imex.IMEXFEval):

  def __init__(self, N, dim=2, L=100.0, nu=1.0, kappa=1.0, **kwoptions):

    if dim != 2:
      raise NotImplementedError

    self.nqvar = N**dim
    self.nfvar = 2*N**dim
    self.N     = N
    self.L     = L
    self.nu    = nu
    self.kappa = kappa
    self.shape = dim*(N,)

    K = 2*math.pi/L * fft.fftfreq(N) * N

    laplacian = np.zeros(self.shape, dtype=np.complex128)
    d_x       = np.zeros(self.shape, dtype=np.complex128)
    d_y       = np.zeros(self.shape, dtype=np.complex128)

    for i in range(N):
      for j in range(N):
        laplacian[i,j] = -(K[i]**2 + K[j]**2)
        d_x[i,j] = K[i] * 1j
        d_y[i,j] = K[j] * 1j

    self.d_x = d_x
    self.d_y = d_y
    self.lap = laplacian

    self.full, self.half = spectral_periodic_masks(dim, N)


  def f1_evaluate(self, y, t, f1, **kwargs):

    z = np.reshape(y, self.shape)

    z_x = self.d_x * z
    z_y = self.d_y * z

    u_x = np.real(fft.ifftn(z_x))
    u_y = np.real(fft.ifftn(z_y))

    z = fft.fftn(-0.5 * (np.square(u_x) + np.square(u_y)))    

    f1[:] = z.flatten()
    f1[0] = 0.0


  def f2_evaluate(self, y, t, f2, **kwargs):

    nu    = self.nu
    kappa = self.kappa
    lap   = self.lap

    z = np.reshape(y, self.shape)

    op = -nu*lap - kappa*lap**2
    z  = op * z

    f2[:] = z.flatten()
    f2[0] = 0.0


  def f2_solve(self, rhs, y, t, dt, f2, **kwargs):

    nu    = self.nu
    kappa = self.kappa
    lap   = self.lap

    z = np.reshape(rhs, self.shape)
    invop = 1.0 / (1.0 + nu*dt*lap + kappa*dt*lap**2)
    z = invop * z

    y[:] = z.flatten()

    op = -nu*lap - kappa*lap**2
    z  = op * z

    f2[:] = z.flatten()
    f2[0] = 0.0


######################################################################
# define interpolator and restrictor

def interpolate(yF, yG, fevalF, fevalG, **kwargs):

  if yF.shape == yG.shape:
    yF[:] = yG[:]
    return

  zG = np.reshape(yG, fevalG.shape)
  zF = np.zeros(fevalF.shape, yG.dtype)

  zF[fevalF.half] = zG[fevalG.full]

  yF[:] = zF.flatten()*4.0


def restrict(yF, yG, fevalF, fevalG, **kwargs):

  if yF.shape == yG.shape:
    yG[:] = yF[:]
    return

  zF = np.reshape(yF, fevalF.shape)
  zG = np.zeros(fevalG.shape, yF.dtype)

  zG[fevalG.full] = zF[fevalF.half]

  yG[:] = zG.flatten()/4.0
