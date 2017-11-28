# ---------------------------------------------------------------------------------
# Constant Correlations
# ---------------------------------------------------------------------------------
import numpy as np

def constantCorrMat(size, rho):
    temp_mat = np.ones((size, size)) * rho
    di = np.diag_indices(size)
    temp_mat[di] = 1.
    return temp_mat