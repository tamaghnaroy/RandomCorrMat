# ----------------------------------------------------
# Generate a random correlations
# ----------------------------------------------------
import numpy as np
import scipy.linalg

def randCorr(size, betaparam=None, m=None):
    """
    Create a random matrix T from uniform distribution of dimensions size x m (assumed to be 10000)
    normalize the rows of T to lie in the unit sphere  r = r / sqrt(r'r)
    RandCorr = TT'

    A direct implementation of this method however, leads to correlation matrix which is almost diagonal.

    @param size: size of the matrix
    @param lower: lower limit of the uniform distribution used to create the corr matrix
    @param upper: upper limit of the uniform distribution used to create the corr matrix
    @return: numpy ndarray, correlation matrix
    """
    # m = 1000
    if m is None:
        m = max([2 * size, 20])
    if betaparam is None:
        betaparam = 0.42
    randomMatrix = np.random.randn(size, m)
    # randomMatrix = np.random.beta(dist_param, dist_param, (size, m))*(upper - lower) + lower
    norms = np.sum(randomMatrix**2, axis=1)
    T = np.divide(randomMatrix, np.sqrt(norms).reshape(size,1))
    alpha = 2 * np.random.beta(betaparam, betaparam, (size, 1)) - 1
    T = np.multiply(T, np.sqrt(1 - np.abs(alpha) ** 2))
    c = np.dot(T, T.T)
    c = np.dot(alpha, alpha.T) + c
    c[np.diag_indices(size)] = 1.
    return c


def randCorrOnion(size):
    """
    This algorithm samples exactly and very quickly from a uniform distribution over the space of correlation matrices.

    The idea here is to build the correlation matrix recursively

    Corr(dimension=d) = [Corr(dimension=d-1) q; q 1]

    q is chosen by the algorithm to ensure that it is a valid correlation matrix

    original paper: https://people.orie.cornell.edu/shane/pubs/NORTAHighD.pdf
    matlab code: https://stats.stackexchange.com/questions/2746/how-to-efficiently-generate-random-positive-semidefinite-correlation-matrices/125017#125017

    For more undestanding Goto OneNote Notebook:
    Portfolio, Clustering .. -> Correlation Matrices -> Random Correaltion

    @param size: size of the correlation matrix
    @param betaparam: a parameter controlling the distributions from which the partial correaltion are chosen
    @return: correlation matrix (size x size)
    """
    S = [[1]]
    for i in range(1, size):
        k = i + 1
        if k == size:
            y = np.random.uniform(0, 1)
        else:
            y = np.random.beta((k-1)/2, (size-k)/2)
        r = np.sqrt(y)
        theta = np.random.randn(k-1, 1)
        theta = theta / np.sqrt(np.dot(theta.T, theta))
        w = r * theta
        R = scipy.linalg.sqrtm(S)
        q = np.dot(R, w)
        S = np.vstack((np.hstack((S, q)),np.hstack((q.T, [[1]]))))
    return S


def randCorrFactor(size, num_factors):
    """
    The idea is to randomly generate several (k<d) factor loadings W (random matrix of k×d size),
    form the covariance matrix WW' (which of course will not be full rank) and add to it a
    random diagonal matrix D with positive elements to make B=WW'+D full rank.

    The resulting covariance matrix can be normalized to become a correlation matrix,
    by letting C=E^(−1/2)*B*E(−1/2), where E is a diagonal matrix with the same diagonal as B.

    @param size: size of the correlation matrix
    @param num_factors: number of factors governing the correlation matrix
    @return:
    """
    W = np.random.normal(size=(size, num_factors))
    S = np.dot(W, W.T) + np.diag(np.random.rand(1, num_factors))
    S = np.dot(np.diag(1 / np.sqrt(np.diag(S))), np.dot(S, np.diag(1 / np.sqrt(np.diag(S)))))
    return S