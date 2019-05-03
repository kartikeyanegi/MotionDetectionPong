from scipy.ndimage.filters import convolve as filter2
from typing import Tuple
import numpy as np
import cv2

HSKERN = np.array([[1/12, 1/6, 1/12],
                   [1/6,    0, 1/6],
                   [1/12, 1/6, 1/12]], float)

kernelX = np.array([[-1, 1],
                    [-1, 1]]) * .25  # kernel for computing d/dx

kernelY = np.array([[-1, -1],
                    [1, 1]]) * .25  # kernel for computing d/dy

kernelT = np.ones((2, 2))*.25


def HornSchunck(im1: np.ndarray, im2: np.ndarray, alpha: float=0.001, Niter: int=8,
                verbose: bool=False) -> Tuple[np.ndarray, np.ndarray]:
    """
    im1: image at t=0
    im2: image at t=1
    alpha: regularization constant
    Niter: number of iteration
    """
    im1 = im1.astype(np.float32)
    im2 = im2.astype(np.float32)

    # set up initial velocities
    uInitial = np.zeros([im1.shape[0], im1.shape[1]])
    vInitial = np.zeros([im1.shape[0], im1.shape[1]])

    # Set initial value for the flow vectors
    U = uInitial
    V = vInitial

    # Estimate derivatives
    [fx, fy, ft] = computeDerivatives(im1, im2)

    if verbose:
        from .plots import plotderiv
        plotderiv(fx, fy, ft)
#    print(fx[100,100],fy[100,100],ft[100,100])

        # Iteration to reduce error
    for _ in range(Niter):
        # %% Compute local averages of the flow vectors
        uAvg = filter2(U, HSKERN)
        vAvg = filter2(V, HSKERN)
        der = (fx*uAvg + fy*vAvg + ft) / (alpha**2 + fx**2 + fy**2)
        U = uAvg - fx * der
        V = vAvg - fy * der

    return U, V


def computeDerivatives(im1: np.ndarray, im2: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

    fx = filter2(im1, kernelX) + filter2(im2, kernelX)
    fy = filter2(im1, kernelY) + filter2(im2, kernelY)

    # ft = im2 - im1
    ft = filter2(im1, kernelT) + filter2(im2, -kernelT)

    return fx, fy, ft

def get_gradient(img1,img2,thresh=None):
    """
    get the magnitude of movement gradient as the same shape as the input images.
    args:
        img1: np array with two channels(grayscale)
        img2: np array same shape as img1
        thresh: gradient threshold to return a binary image, 
        if it is none return gradient information as is without thresholding.
    """
    import time
    
    u,v = HornSchunck(img1,img2)

    m,n = img1.shape
    grad = np.zeros((m,n))
    init_time = time.time()
    
    magn = np.sqrt(np.power(u,2)+np.power(v,2))
    #print ("np time",time.time()-init_time)
    if thresh is None:
        grad=magn
        #print(magn.mean())
        #grad[np.where(magn>0)]=255
    else:
        grad[np.where(magn>thresh)]=255
    """
    init_time = time.time()
    for i in range(m):
        for j in range(n):
            g = (u[i,j]**2+v[i,j]**2)**0.5
            if thresh is None:
                grad[i,j]=g

                continue
            if g >thresh:
                grad[i,j]=255
    print ("for time",time.time()-init_time)
    """
    return grad