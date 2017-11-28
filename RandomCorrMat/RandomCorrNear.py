import numpy as np
import numpy.linalg as LA


def proj_spd(A):
    # NOTE: the input matrix is assumed to be symmetric
    d, v = np.linalg.eigh(A)
    A = (v * np.maximum(d, 0)).dot(v.T)
    A = (A + A.T) / 2
    return A

def proj_unitdiag(A):
    n = A.shape[0]
    A[np.diag_indices(n)] = 1
    return A

def nearcorr(A, max_iterations=100, weights=None):
    """
    Finds the nearest correlation matrix to the symmetric matrix A.

    @param A: symmetric numpy array (n x n)
    @param max_iterations: is the maximum number of iterations (default 100)
    @param weights: weights for the rows of the matrix A
    @return: Correlation matrix

    Note:
    This is a partial working port of the original MATLAB code by N. J. Higham,
    https://nickhigham.wordpress.com/2013/02/13/the-nearest-correlation-matrix/

    Reference:  N. J. Higham, Computing the nearest correlation matrix---A problem from finance. IMA J. Numer. Anal.,
    22(3):329-343, 2002.
    """
    eps = np.finfo(np.float64).eps
    tol = eps * np.shape(A)[0] * np.ones(2)
    weights = np.ones(np.shape(A)[0]) if not weights else weights
    X = Y = A
    rel_diffY = rel_diffX = rel_diffXY = np.inf
    ds = np.zeros_like(A)
    Whalf = np.sqrt(np.outer(weights, weights))

    iteration = 0
    while max(rel_diffX, rel_diffY, rel_diffXY) > tol[0]:
        iteration += 1
        if iteration > max_iterations:
            return X

        Xold = X.copy()
        R = X - ds
        R_wtd = Whalf*R
        X = proj_spd(R_wtd)

        X = X / Whalf
        ds = X - R
        Yold = Y.copy()
        Y = proj_unitdiag(X)
        normY = LA.norm(Y, 'fro')
        rel_diffX = LA.norm(X - Xold, 'fro') / LA.norm(X, 'fro')
        rel_diffY = LA.norm(Y - Yold, 'fro') / normY
        rel_diffXY = LA.norm(Y - X, 'fro') / normY

    return X







