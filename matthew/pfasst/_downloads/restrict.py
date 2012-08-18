
import numpy as np

def restrict(yF, yG, fevalF=None, fevalG=None, **kwargs):
  '''Restrict yF to yG.'''


  Nx, Ny, Nc = fevalG.shape

  qF = np.reshape(yF, fevalF.shape)
  qG = np.zeros(fevalG.shape)

  for i in range(Nx):
    for j in range(Ny):
      qG[i,j,:] += ( qF[2*i+0,2*j+0,:] +
                     qF[2*i+0,2*j+1,:] +
                     qF[2*i+1,2*j+0,:] +
                     qF[2*i+1,2*j+1,:] )

  yG[:] = qG.flatten() / 4.0
