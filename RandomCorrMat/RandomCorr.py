# ----------------------------------------------------
# Generate a random correlations
# ----------------------------------------------------
import numpy as np

def randCorr(size, lower=-1, upper=1):
    """
    Create a random matrix T from uniform distribution of dimensions size x m (assumed to be 10000)
    normalize the rows of T to lie in the unit sphere  r = r / sqrt(r'r)
    RandCorr = TT'

    @param size: size of the matrix
    @param lower: lower limit of the uniform distribution used to create the corr matrix
    @param upper: upper limit of the uniform distribution used to create the corr matrix
    @return: numpy ndarray, correlation matrix
    """
    m = 1000
    randomMatrix = np.random.uniform(lower, upper, (size, m))
    norms = np.sum(randomMatrix**2, axis=1)
    T = np.divide(randomMatrix, np.sqrt(norms).reshape(size,1))
    c = np.dot(T, T.T)
    c[np.diag_indices(size)] = 1.
    return c
