'''Solve the 1d wave equation with PyPFASST.'''

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


###############################################################################
# WAVE FEval

class WAVE(pfasst.imex.IMEXFEval):
  '''FEval class for the 1d wave equation.'''

  def __init__(self, N, L=1.0, **kwargs):

    self.nqvar = 2*N
    self.nfvar = 4*N
    self.N     = N
    self.L     = L

    shape = (N,2)

    # frequencies = 2*pi/L * (wave numbers)
    K = 2*math.pi/L * fft.fftfreq(N) * N
    self.ddx = K*1j

    # spectral interpolation masks
    self.full, self.half = spectral_periodic_masks(1, N)

    self.shape = shape


  def f1_evaluate(self, y, t, f1, **kwargs):
    '''Evaluate explicit piece.'''

    u = np.reshape(y, self.shape)

    z1 = fft.fft(u[:,0])
    z2 = fft.fft(u[:,1])

    z1_x = self.ddx * z1
    z2_x = self.ddx * z2

    u1_x = np.real(fft.ifft(z1_x))
    u2_x = np.real(fft.ifft(z2_x))

    f = np.zeros(self.shape)
    f[:,0] = u2_x
    f[:,1] = u1_x

    f1[:] = f.flatten()


###############################################################################
# define interpolator and restrictor

def interpolate(yF, yG, fevalF=None, fevalG=None, **kwargs):
  '''Interpolate yG to yF.'''

  if fevalF.shape == fevalG.shape:
    yF[:] = yG[:]
    return

  uF = np.zeros(fevalF.shape)
  uG = np.reshape(yG, fevalG.shape)

  for n in (0, 1):
    zG = fft.fft(uG[:,n])
    zF = np.zeros(fevalF.N, zG.dtype)

    zF[fevalF.half] = zG[fevalG.full]

    uF[:,n] = np.real(2*fft.ifft(zF))

  yF[:] = uF.flatten()


def restrict(yF, yG, fevalF=None, fevalG=None, **kwargs):
  '''Restrict yF to yG.'''

  if fevalF.shape == fevalG.shape:
    yG[:] = yF[:]
    return

  uG = np.zeros(fevalG.shape)
  uF = np.reshape(yF, fevalF.shape)

  uG[:,:] = uF[::2,:]

  yG[:] = uG.flatten()


