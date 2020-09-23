# ---------------------------------------------------------------------------------
# Random correlation Matrix with Specified eigenvalues
# http://www.maths.manchester.ac.uk/~higham/narep/narep354.pdf  (DAVIES & HIGHAM)
# Appendix_C_Generating_Random_Correlation_Matrices             (Explains Stewart method for orthogonal transforms)
# ---------------------------------------------------------------------------------

import numpy as np

def sgn(A):
    """
    Utility function to return the sign of the matrix values, basically a longer version of np.sign()

    @param A: numpy nxn ndarray
    @return: sign of the array
    """
    if isinstance(A, np.ndarray):
        B = A.copy()
        B[B>0] = 1
        B[B<0] = -1
        return B
    elif isinstance(A, float):
        A = np.array([A])
        B = A.copy()
        B[B > 0] = 1
        B[B < 0] = -1
        return B
    else:
        raise Exception()


def randOrthog(n, f = np.random.randn):
    """
    Use stewart's algorithm to create a n x n random orthogona matrix

    @param n: size = num rows = num cols
    @param f: function to use for generating random, np.random.randn or np.random.rand
    @return: numpy nxn ndarray 
    """
    A = np.eye(n) # n x n
    d = np.zeros((n,1)) # n x 1
    d[n-1, 0] = sgn(f(1, 1))
    for k in range(n-2,-1,-1):
        x = f(n-k, 1)  #n-k+1 x 1
        s = np.sqrt(np.dot(x.T, x))
        sg = np.sign(x[0, 0])
        s = sg*s
        d[k,0] = -sg
        x[0, 0] = x[0, 0] + s
        beta = s * x[0, 0]
        y = np.dot(x.T, A[k:,:])
        A[k:, :] = A[k:,:] - x*(y/beta)
    A = d*A
    return A


def randMatwithEigenVals(lamb, f = np.random.randn):
    """
    Use stewart algorithm to produce a random orthogonal matrix P and then create the matrix with given algorithm
    by using P' diag(lamb) P

    @param lamb: eigenvalues (sorted)
    @param f: function for random generator -- either np.random.randn or np.random.rand
    @return: numpy ndarray (size = size of eigenvalues)

    """
    n = len(lamb)
    Q = randOrthog(n, f)
    return np.dot(Q.T, np.dot(np.diag(lamb), Q))


def applyGivens(A, i, j):
    """
    apply Givens rotation to A in (i, j) position. Naive implementation is
    G = I(nrow(A));
    G[i, i] = c;
    G[i, j] = s;
    G[j, i] = -s;
    G[j, j] = c;
    A = G' * A * G;
    @param A: numpy ndarray (n x n)
    @param i: row id
    @param j: col id
    @return:  A with the Givens rotation
    """
    Aii = A[i, i]
    Aij = A[i, j]
    Ajj = A[j, j]
    t = (Aij + np.sqrt(Aij**2 - (Aii-1)*(Ajj-1))) / (Ajj-1)
    c = 1 / np.sqrt(1 + t**2)
    s = c * t
    G = np.eye(A.shape[0])
    G[i, i] = c
    G[i, j] = s
    G[j, i] = -s
    G[j, j] = c
    return np.dot(G.T, np.dot(A, G))


def randCorrGivenEgienvalues(lamb, f = np.random.randn):
    """
    Create a random matrix with eigenvlaues lamb and then apply Givens rotations to convert the matrix to a corr matrix

    @param lamb: numpy vector (sorted)
    @param f: function for random number generator, either np.random.randn or np.random.rand
    @return: numpy ndarray (corr mat)
    """
    n = len(lamb)
    lamb = np.reshape(lamb, (1, len(lamb)))
    lamb = n * lamb / np.sum(lamb)

    corr = randMatwithEigenVals(np.ravel(lamb), f)
    corr = (corr + corr.T)/2
    n_iters = 0
    while np.sum(corr[np.diag_indices(n)]) !=n:
        corr = randMatwithEigenVals(np.ravel(lamb))
        corr = (corr + corr.T) / 2
        n_iters += 1
        if n_iters >20:
            raise Exception('Could Not Construct a valid corr matrix such that trace(corr) == n')

    convergence= False
    iter = 0
    while not convergence :
        if iter > n:
            break
        # Collect the diagonal and ensure that trace(corr) = n
        d = corr[np.diag_indices(n)]
        if np.abs(np.sum(d) - n)>1e-6:
            raise Exception('trace of corr is not equal to n, trace = %s, diagnal terms = [%s], iteration = %s' % (np.sum(d), d, iter))

        if all(abs(d-1) < 1e-6):
            convergence = True
            break
        else:
            # Apply Givens Transformation
            idx = np.arange(n)
            idxgt1 = idx[d>1]
            idxlt1 = idx[d<1]

            i = idxlt1[0]
            j = idxgt1[-1]
            if i > j:
                i = idxgt1[0]
                j = idxlt1[-1]
            trace_sum = corr[i, i] + corr[j, j]
            corr = applyGivens(corr, i, j)
            corr[i, i] = 1.
            corr[j, j] = trace_sum - 1.
        iter += 1
    C = np.round(corr,4)
    C[np.diag_indices(C.shape[0])] = 1
    return C