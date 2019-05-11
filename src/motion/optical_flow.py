from scipy.ndimage.filters import convolve
import numpy as np

def HornSchunck(old_img, new_img, lamb=10, num_iters=8):
    ## Roberts derivative kernels
    Mx = np.array([[0, 1],
                  [-1, 0]])  # kernel for computing d/dx

    My = np.array([[1, 0],
                  [0, -1]])  # kernel for computing d/dy

    ## Kernel for calculating U and V mean
    K_avg = np.array([[0   , .25 , 0],
                     [.25 ,  0  ,.25],
                     [0   , .25 , 0]], float)

    old_img = old_img.astype(np.float32)
    new_img = new_img.astype(np.float32)
    m,n = new_img.shape

    # Estimate derivatives
    Ex = convolve(new_img, Mx)
    Ey = convolve(new_img, My)
    Et = new_img-old_img

    ###### Initinialize values of u,v with zero
    u = np.zeros((m,n))
    v = np.zeros((m,n))

    for _ in range(num_iters):
        u_mean = convolve(u, K_avg)
        v_mean = convolve(v, K_avg)
        alpha = lamb*(Ex*u_mean + Ey*v_mean + Et) / (1+lamb*(Ex**2 + Ey**2))
        u = u_mean - alpha * Ex 
        v = v_mean - alpha * Ey
    return u, v

def get_gradient(old_img,new_img,thresh=None):
    u,v = HornSchunck(old_img,new_img)
    magn = np.sqrt(np.power(u,2)+np.power(v,2))
    gradient = np.zeros_like(old_img)
    gradient[np.where(magn>thresh)]=255
    return gradient