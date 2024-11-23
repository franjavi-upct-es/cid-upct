# método de Jacobi

import numpy as np

def jacobi(A, b, tolerance=1e-10, max_iterations=10000):
    
    x = np.zeros_like(b, dtype=np.double)
    
    T = A - np.diag(np.diagonal(A))
    
    for k in range(max_iterations):
        
        x_old  = x.copy()
        
        x[:] = (b - np.dot(T, x)) / np.diagonal(A)

        num_error = np.linalg.norm(x - x_old, ord=np.inf)
        den_error = np.linalg.norm(x, ord=np.inf)        
        error =  num_error / den_error 
        
        if error < tolerance:
            break
            
    return x