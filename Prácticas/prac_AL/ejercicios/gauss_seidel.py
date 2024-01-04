# método de Gauss-Seidel

import numpy as np

def gauss_seidel(A, b, tolerance=1e-10, max_iterations=10000):
    
    x = np.zeros_like(b, dtype=np.double)
    
    #Iteraciones
    for k in range(max_iterations):
        
        x_old  = x.copy()
        
        # bucle sobre las filas
        for i in range(A.shape[0]):
            x[i] = (
                b[i] - np.dot(A[i,:i], x[:i]) 
                - np.dot(A[i,(i+1):], x_old[(i+1):])
                ) / A[i ,i]
            
        # condición de parada

        num_error = np.linalg.norm(x - x_old, ord=np.inf)
        den_error = np.linalg.norm(x, ord=np.inf)
        error =  num_error / den_error 
        
        if  error < tolerance:
            break
            
    return x