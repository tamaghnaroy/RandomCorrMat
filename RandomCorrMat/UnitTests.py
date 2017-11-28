import unittest
import numpy as np

from .ConstantCorr import *
from .Diagnostics import *
from .RandomCorr import *
from .RandomCorrMatEigen import *
from .RandomCorrNear import *
from .RandomPerturb import *

class TestRandCorr(unittest.TestCase):
    # test diagnostics functions
    def test_valid_corr(self):
        A = np.array([[1, 2],[0, 1]])
        res = isvalid_corr(A)
        self.assertFalse(res)
        self.assertEqual(res.cause, ['Not symmetric', 'Off Diagonal outside [-1, 1]'])

    def test_valid_corr2(self):
        A = np.array([[1, 1, 0.99],[1, 1, 0], [0.99, 0, 1]])
        res = isvalid_corr(A)
        self.assertFalse(res)
        self.assertEqual(res.cause, ['Not Positive Definite'])

    # Test Random Corr
    def test_random_corr(self):
        A = randCorr(10)
        self.assertTrue(isvalid_corr(A), True)

    def test_random_corr_limits(self):
        A = randCorr(5,lower=-0.25, upper=0.5)
        self.assertTrue(np.min(A)>=-0.25, True)
        self.assertTrue(np.max(A - np.eye(5)) <= 0.5, True)

    # Test Constant Corr
    def test_constant_corr(self):
        A = constantCorrMat(5, 0.99)
        self.assertTrue(isvalid_corr(A))

    # Test Correlation Matrices with given Eigenvalues
    def test_rand_orthog(self):
        Q = randOrthog(10)
        self.assertTrue(np.allclose(np.dot(Q.T, Q), np.eye(10), rtol=1e-05, atol=1e-08))

    def test_randMatwithEigen(self):
        lamb = np.array([2, 1, 0.75, 0.25])
        A = randMatwithEigenVals(lamb)
        self.assertAlmostEqual(np.trace(A), np.sum(lamb), places=10)  # trace(A) = n
        self.assertTrue(np.allclose(LA.eigvalsh(A), np.sort(lamb), rtol=1e-05, atol=1e-08))

    def test_givens(self):
        lamb = np.array([2, 1, 0.75, 0.25])
        Q = randMatwithEigenVals(lamb)
        J = applyGivens(Q, 2, 3)
        self.assertAlmostEqual(Q[0,0], J[0,0], places=16)
        self.assertAlmostEqual(Q[1, 1], J[1, 1], places=16)
        self.assertEqual(J[2,2], 1.0)
        self.assertAlmostEqual(np.trace(J), 4.0, places=10)

    def test_randcorrwitheigenvalue(self):
        e = np.r_[2, 1, 0.75, 0.25]
        corr_mat = randCorrGivenEgienvalues(e)
        self.assertTrue(isvalid_corr(corr_mat))
        self.assertTrue(np.allclose(LA.eigvalsh(corr_mat), np.sort(e), rtol=1e-02, atol=1e-08))

    # Test Nearest Corr
    def test_near_corr(self):
        A = np.array([[1, 1, 0],
                      [1, 1, 1],
                      [0, 1, 1]])

        X = nearcorr(A)

        expected_result = np.array([[1., 0.7607, 0.1573],
                                    [0.7607, 1., 0.7607],
                                    [0.1573, 0.7607, 1.]])

        # print(np.abs((X - expected_result))/1e-5)
        self.assertTrue((np.abs((X - expected_result)) < 2e-5).all())

    # Perturb Correlation Matrix
    def test_perturb_corr(self):
        corr_mat = np.array([[1, 0.5, 0.75],[0.5, 1, 0.75], [0.75, 0.75, 1]])
        new_corr = perturb_randCorr(corr_mat)
        obj = isvalid_corr(new_corr)
        self.assertTrue(obj)