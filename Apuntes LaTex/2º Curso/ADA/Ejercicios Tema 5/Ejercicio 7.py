import numpy as np

def optimal_job_sequence(B, m):
    n = len(B)
    # Inicializar tablas dp y prev
    dp = np.zeros((m + 1, n))
    prev = np.full((m + 1, n), -1)

    # Llenar la tabla dp
    for k in range(2, m + 1): # Desde la segunda iteración
        for j in range(n): # Último trabajo en la secuencia
            max_benefit = -float('inf')
            best_prev = -1
            for i in range(n): # Penúltimo trabajo en la secuencia
                benefit = dp[k-1][i] + B[i][j]
                if benefit > max_benefit:
                    max_benefit = benefit
                    best_prev = i
            dp[k][j] = max_benefit
            prev[k][j] = best_prev

    # Encontrar el máximo beneficio de dp[m]
    max_benefit = -float('inf')
    last_job = -1
    for j in range(n):
        if dp[m][j] > max_benefit:
            max_benefit = dp[m][j]
            last_job = j

    # Reconstruir la secuencia óptima
    sequence = []
    k = m
    while k > 0 and last_job != -1:
        sequence.append(last_job)
        last_job = prev[k][last_job]
        k -= 1
    sequence.reverse()

    return max_benefit, sequence

# Matriz de beneficios
B = np.array([
    [2, 2, 5], # Beneficios desde a
    [4, 1, 3], # Beneficios desde b
    [3, 2, 2]  # Beneficios desde c
])

# Número de tabajos en la secuencia
m = 5

# Ejecutar el algoritmo
max_benefit, sequence = optimal_job_sequence(B, m)
print(f"Beneficio máximo: {max_benefit}")
print(f"Secuencia óptima: {sequence}")
