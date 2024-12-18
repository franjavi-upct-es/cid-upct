def binom_rec(n, m):
    if m == 0 or m == n:
        return 1
    return binom_rec(n-1, m) + binom_rec(n-1, m-1)

def binom_dp(n, m):
    # Crear la tabla dp
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    # Condiciones base
    for i in range(n + 1):
        dp[i][0] = 1  # Caso m = 0
        if i <= m:
            dp[i][i] = 1  # Caso m = n

    # Llenar la tabla
    for i in range(1, n + 1):
        for j in range(1, min(i, m + 1)):
            dp[i][j] = dp[i - 1][j] + dp[i - 1][j - 1]

    return dp[n][m]

# Ejemplo de uso
n, m = 5, 2
print(f"Resultado con recursión: {binom_rec(n, m)}")
print(f"Resultado con DP: {binom_dp(n, m)}")