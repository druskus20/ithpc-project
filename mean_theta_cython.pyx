import numpy as np
cimport numpy as np

cimport cython
from libc.math cimport atan2, cos, sin, pow
from libc.stdlib cimport rand, RAND_MAX

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef mean_theta_c(np.ndarray[np.float64_t, ndim=2] theta,
                            np.ndarray[np.float64_t, ndim=2] x,
                            np.ndarray[np.float64_t, ndim=2] y,
                            double R,
                            np.ndarray[np.float64_t, ndim=2] mean_theta):
                            
    cdef Py_ssize_t N = theta.shape[0]
    cdef Py_ssize_t b, i
    cdef double sx, sy

    for b in range(N):
        sx = 0
        sy = 0
        for i in range(N):
            if (x[b, 0] - x[i, 0]) ** 2 + (y[b, 0] - y[i, 0]) ** 2 < R ** 2:
                sx += cos(theta[i, 0])
                sy += sin(theta[i, 0])

        mean_theta[b, 0] = atan2(sy, sx)


