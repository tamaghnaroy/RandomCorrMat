import numpy as np
from numpy import linalg as LA

# --------------------------------------------------------------------------------
# Diagnostics
# --------------------------------------------------------------------------------

class CorrDiagnostics(object):
    def __init__(self, corrmat):
        self.symmetric = np.all(corrmat == corrmat.T)
        self.pd = isPD(corrmat)
        self.off_diagonal = np.all(np.abs(corrmat)<=1)
        self.diagonal = np.all(corrmat[np.diag_indices(corrmat.shape[0])]==1)

        self.valid = self.symmetric and self.diagonal and self.off_diagonal and self.pd

        self.problems = ['Not symmetric', 'Not Positive Definite', 'Off Diagonal outside [-1, 1]', 'Diagonal != 1']
        self.metric_vals = [self.symmetric, self.pd, self.off_diagonal, self.diagonal]
        self._cause = [b[0] for b in zip(self.problems, self.metric_vals) if not b[1]]

    def __nonzero__( self) :
        return bool(self.valid)

    def __bool__( self) :
        return bool(self.valid)

    @property
    def cause(self):
        return self._cause

def isPD(corrmat):
    """
    Check if all the eigenvalues of the matrix are greater than zero

    @param corrmat: numpy n x n ndarray
    @return: bool
    """
    lambdas = LA.eigvalsh(corrmat)
    return all(lambdas>0)

def isvalid_corr(corrmat):
    """
    Check if
    1. corrmat is symmetric
    2. off-diagonal values in [-1, 1]
    3. diagonal values = 1
    4. the matrix is positive semidefinite.

    @param corrmat: numpy nxn ndarray
    @return: CorrDiagnostics object ---> evaluates to True if corrmat is valid and False otherwise, .cause gives the cause
    """
    return CorrDiagnostics(corrmat)