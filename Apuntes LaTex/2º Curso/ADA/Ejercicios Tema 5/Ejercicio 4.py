def subset_sum(A, K):
    n = len(A)
    # Crear tabla DP
    dp = [[False for _ in range(K + 1)] for _ in range(n + 1)]

    # Caso base
    for i in range(n + 1):
        dp[i][0] = True # Sumar 0 siempre es posible

    # Llenar la tabla DP
    for i in range(1, n + 1):
        for j in range(K + 1):
            dp[i][j] = dp[i-1][j] # No incluir el elemento actual
            if j >= A[i-1]: # Incluir el elemento actual si cabe
                dp[i][j] = dp[i][j] or dp[i-1][j - A[i-1]]

    # La solución está en dp[n][K]
    return dp, dp[n][K]

# Ejemplo
A = [2, 3, 5, 2]
K = 7
dp, exists = subset_sum(A, K)
print(f"¿Existe una solución? {exists}")

def find_subset(dp, A, K):
    n = len(A)
    subset = []
    i, j = n, K

    while i > 0 and j > 0:
        # Si el elemento está incluido
        if dp[i][j] != dp[i-1][j]:
            subset.append(A[i-1])
            j -= A[i-1]
        i -= 1
    return subset

# Obtener el subconjunto
subset = find_subset(dp, A, K)
print(f"Subconjunto encontrado: {subset}")
