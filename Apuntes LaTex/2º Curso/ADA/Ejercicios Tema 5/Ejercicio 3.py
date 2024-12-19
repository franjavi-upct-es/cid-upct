def count_ways_to_fill_knapsack(n, M, p):
    # Crear la tabla DP
    dp = [[0 for _ in range(M+ 1 )] for _ in range(n + 1)]

    # Inicial el caso base
    for i in range(n + 1):
        dp[i][0] = 1    # Una forma de llenar peso 0 (mochila vacía)

    # LLenar la tabla DP
    for i in range(1, n + 1):
        for w in range(M + 1):
            dp[i][w] = dp[i - 1][w] # No tomar el objeto i
            if w >= p[i - 1]: # Si cabe el objeto i
                dp[i][w] += dp[i - 1][w - p[i - 1]]

    # Sumar todas las formas válidas
    return sum(dp[n])

# Datos de ejemplo
n = 3 # Número de objetos
M = 4 # Capacidad de la mochila
p = [1, 2, 3] # Pesos de los objetos

print(f"Número de formas de llenar la mochila: {count_ways_to_fill_knapsack(n, M, p)}")