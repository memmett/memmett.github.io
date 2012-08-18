
import numpy as np

def interpolate(yF, yG, fevalF=None, fevalG=None, **kwargs):
  '''Interpolate yG to yF.'''

  Nx, Ny, Nc = fevalG.shape
  Ng = fevalG.Ng
  Nq = 6

  qF = np.zeros(fevalF.shape)
  qG = np.reshape(yG, fevalG.shape)

  qr = np.zeros((Nx+2*Ng,Ny+2*Ng,Nc,Nq,Nq))
  qg = np.zeros((Nx+2*Ng,Ny+2*Ng,Nc))

  w = np.array([5.0/9.0, 8.0/9.0, 5.0/9.0])

  qg[ Ng:-Ng, Ng:-Ng, :] = qG[   :  ,   :  , :]
  qg[   :Ng , Ng:-Ng, :] = qG[-Ng:  ,   :  , :]
  qg[-Ng:   , Ng:-Ng, :] = qG[   :Ng,   :  , :]    
  qg[Ng:-Ng,    :Ng , :] = qG[   :  ,-Ng:  , :]
  qg[Ng:-Ng, -Ng:   , :] = qG[   :  ,   :Ng, :]

  qr = np.zeros((Nx+2*Ng,Ny+3*Ng,Nc,Nq,Nq)) # volume: i, j, c, li, lj

  for c in range(Nc):
    fevalG.reconstructor.reconstruct_volume(qg[:,:,c], qr[:,:,c,:,:])

  qr = qr[Ng:-Ng+1,Ng:-Ng+1,:,:,:]
  tmp = np.zeros(3)

  for i in range(Nx):
    for j in range(Ny):
      for c in range(Nc):

        tmp[0] = np.dot(w, qr[i,j,c,:3,0])
        tmp[1] = np.dot(w, qr[i,j,c,:3,1])
        tmp[2] = np.dot(w, qr[i,j,c,:3,2])
        
        qF[2*i+0,2*j+0,c] = np.dot(w, tmp)
        acc = qF[2*i+0,2*j+0,c]

        tmp[0] = np.dot(w, qr[i,j,c,3:,0])
        tmp[1] = np.dot(w, qr[i,j,c,3:,1])
        tmp[2] = np.dot(w, qr[i,j,c,3:,2])
        
        qF[2*i+1,2*j+0,c] = np.dot(w, tmp)
        acc += qF[2*i+1,2*j+0,c]

        tmp[0] = np.dot(w, qr[i,j,c,:3,3])
        tmp[1] = np.dot(w, qr[i,j,c,:3,4])
        tmp[2] = np.dot(w, qr[i,j,c,:3,5])
        
        qF[2*i+0,2*j+1,c] = np.dot(w, tmp)
        acc += qF[2*i+0,2*j+1,c]

        tmp[0] = np.dot(w, qr[i,j,c,3:,3])
        tmp[1] = np.dot(w, qr[i,j,c,3:,4])
        tmp[2] = np.dot(w, qr[i,j,c,3:,5])
        
        qF[2*i+1,2*j+1,c] = np.dot(w, tmp)
        acc += qF[2*i+1,2*j+1,c]

        # diff = (qG[i,j,c] - acc)/4.0

        # qF[2*i+0,2*j+0,c] += diff
        # qF[2*i+0,2*j+1,c] += diff
        # qF[2*i+1,2*j+0,c] += diff
        # qF[2*i+1,2*j+1,c] += diff
  
  yF[:] = qF.flatten() * 4.0
