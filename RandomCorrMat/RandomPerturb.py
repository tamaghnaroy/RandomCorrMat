# -------------------------------------------------------
# Generate a Perturbation of a given correlation
# ------------------------------------------------------

import numpy as np
from numpy import linalg as LA

from .RandomCorrMatEigen import *

def perturb_randCorr(corr_mat):
    """
    If C is a correlation matrix then C+X is a correlation matrix if and only if 2-norm or 1-norm or inf-norm of X is less than the smallest eigenvalue of C.

    @param corr_mat: numpy ndarray
    @return: perturbed correlation matrix
    """

    # compute the smallest eigenvalue - lambda - of the corr matrix
    eigenvals = LA.eigvalsh(corr_mat)
    lamb = min(eigenvals)
    # Create a random matrix with eigenvalues in [1-lamb, 1+lamb]
    perturb_eigenvalues = np.random.uniform(1-lamb, 1+lamb, corr_mat.shape[0])
    A = randMatwithEigenVals(perturb_eigenvalues)
    # perturbe corr = corr + A - I
    c = corr_mat + A - np.eye(corr_mat.shape[0])
    c[np.diag_indices(c.shape[0])]= 1.
    c = 0.5*(c+c.T)
    return c