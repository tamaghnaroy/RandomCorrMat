# RandomCorrMat
Implements several schemes to generate random correlation matrices, including
checks to validate a given matrix to be a proper correlation matrix.

##### Diagnostics
Diagnostics contain two main methods - isPD and isvalid_corr. These methods
check for the following conditions in a given matrix -
1. The matrix is symmetric
2. Diagonal == 1
3. Off-Diagonal != 1
4. The matrix is positive definite

###### Usage: 
```python
import RandomCorrMat
    
matrix_to_test = [[1 , 0.9 , -0.9], [0.9, 1, 0.25], [-0.9, 0.25, 1]]
    
res = RandomCorrMat.isvalid_corr(matrix_to_test)
res == True         # if the correlation is valid
res == False        # if the correlation is invalid
    
# To fetch more information in case the matrix is an invalid correlation matrix
# we can use the following
    

res.cause
``` 

##### Random Correlation Matrix Generation  
To generate random correlation matrix, there are several schemes:
1. Constant correlation matrix 
2. Simple random matrix
3. Random matrix with given eigenvalues
4. Random perturbation of a given correlation matrix
5. Nearest correlation matrix to a given correlation matrix 

###### Usages
```python
import RandomCorrMat

    
# Generate a constant correlation matrix
RandomCorrMat.constantCorrMat(size, cor_value)
    
     
# Generate a Random correalation matrix sampled uniformly from the space of corelation matrices
RandomCorrMat.randCorrOnion(size)

# Generate the Random correlation matrix, faster but no gaurantees
RandomCorrMat.randCorr(size)

# Generate a random correlation matrix with given eigenvalues
e = numpy.r_[2, 1, 0.75, 0.25]
corr_mat = RandomCorrMat.randCorrGivenEgienvalues(e)
   
    
# Random perturbation of the correlation matrix
given_corr_mat = numpy.array([[1, 0.5, 0.75],[0.5, 1, 0.75], [0.75, 0.75, 1]])
new_corr = RandomCorrMat.perturb_randCorr(given_corr_mat)
    
    
# Perturbation method can be used to generate correlation matrix with a given mean
# For example: to generate a random correlation matrix with average corr = 0.75
corr_mat = RandomCorrMat.constantCorrMat(4, 0.75)
new_corr = RandomCorrMat.perturb_randCorr(corr_mat)
    
    
# The variance of the perturbations obtained from the above method are not 
# sufficiently large, if we want to simulate random correlation with higher 
# variance or we need fine control on the noise added to the correlation matrix
# Example to handle these
    
manual_noisy_corr = given_corr_mat + numpy.random.normal(loc=0.0, scale=3.0, size=(3,3))
valid_corr = RandomCorrMat.nearcorr(manual_noisy_corr)
```

References
----------
* Generating Random Correlation Matrices: 
    https://www.researchgate.net/file.PostFileLoader.html?id=597638823d7f4b385f3f0a45&assetKey=AS%3A519710043275264%401500919938026
* Marsaglia, George, and Ingram Olkin. "Generating correlation matrices." SIAM Journal on Scientific and Statistical Computing 5.2 (1984): 470-475.
* Higham, Nicholas J. "Computing the nearest correlation matrix—a problem from finance." IMA journal of Numerical Analysis 22.3 (2002): 329-343.
* Higham's MATLAB CODE: https://nickhigham.wordpress.com/2013/02/13/the-nearest-correlation-matrix/


Installing from PyPI
--------------------

Try

```pip install RandCorrMat```

To install manually from the git repo, try this:

```python setup.py install```

The RandCorrMat codebase supports Python 2 and 3.


Attribution
-----------

If you happen to use RandCorrMat in your work or research, please cite its GitHub repository:

T. Roy, RandCorrMat, (2017), GitHub repository, https://github.com/tamaghnaroy/RandomCorrMat/


License
-------

RandCorrMat is free software made available under the MIT License. For details see the LICENSE file.