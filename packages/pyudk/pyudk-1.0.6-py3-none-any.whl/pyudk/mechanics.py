import scipy as si
import numpy as np
import sympy as sp

def A_b_Matrices(self,vec:sp.Matrix, coeffs:sp.Matrix):
    '''
        Factorize a vector into the product of a matrix and its coefficients. 

        Parameters
        ----------
        - `vec` : column vector of 2nd order constraint equations in the standard form
        - `q''` : column vector of generalized coordinate to factorize 

        Return
        ------
        - `A` : vec = A@q''
    '''
    A = sp.zeros(len(vec),len(coeffs))
    b = sp.zeros(len(vec),1)
    for i,v in enumerate(vec):
        expr = sp.collect(sp.expand(v), syms=coeffs[:])
        b[i] = expr
        for j,c in enumerate(coeffs):
            A[i,j] = expr.coeff(coeffs[j])
            b[i] = b[i] - (A[i,j]*coeffs[j])
    return A,b  


def ideal_Constraint_force(self, m, q, A, b):
    B = A @ si.linalg.fractional_matrix_power(m, -1 / 2)
    a = si.linalg.inv(m) @ q
    Msqrt = si.linalg.fractional_matrix_power(m, 1 / 2)
    e = b - A @ a  # the error vector
    Bplus = np.linalg.pinv(B.astype(np.float64))
    K = Msqrt @ Bplus  # weighted Moore-Penrose generalized inverse of the weighted constraint matrix A
    return K @ e

def non_ideal_Constraint_force(self,m,A,c):
    M_negsqrt = si.linalg.fractional_matrix_power(m, -1 / 2)
    B = A @ M_negsqrt
    M_sqrt = si.linalg.fractional_matrix_power(m, 1 / 2)
    BplusB = np.linalg.pinv(B.astype(np.float64)) @ B
    I = np.identity(BplusB.shape[0])
    return M_sqrt @ (I - BplusB) @ M_negsqrt @ c
