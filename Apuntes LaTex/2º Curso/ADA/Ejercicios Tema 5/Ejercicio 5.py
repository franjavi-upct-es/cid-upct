def two_knapsacks(n, M1, M2, p, b):
    # Crear tabla DP
    dp = [[[0 for _ in range(M2 + 1)] for _ in range(M1 + 1)] for _ in range(n + 1)]

    # LLenar la tabla DP
    for i in range(1, n + 1):
        for c1 in range(M1 + 1):
            for c2 in range(M2 + 1):
                # No incluir el objeto
                dp[i][c1][c2] = dp[i-1][c1][c2]
                # Incluir en la mochila 1 si cabe
                if c1 >= p[i-1]:
                    dp[i][c1][c2] = max(dp[i][c1][c2], dp[i-1][c1 - p[i-1]][c2] + b[i-1])
                # Incluir en la mochila 2 si cabe
                if c2 >= p[i-1]:
                    dp[i][c1][c2] = max(dp[i][c1][c2], dp[i-1][c1][c2 - p[i-1]] + b[i-1])

    return dp, dp[n][M1][M2]

# Reconstrucción de la solución
def find_items(dp, n, M1, M2, p, b):
    items_in_knapsack1 = []
    items_in_knapsack2 = []
    c1, c2 = M1, M2

    for i in range(n, 0, -1):
        if dp[i][c1][c2] != dp[i-1][c1][c2]:
            if c1 >= p[i-1] and dp[i][c1][c2] == dp[i-1][c1 - p[i-1]][c2] + b[i-1]:
                items_in_knapsack1.append(i-1)
                c1 -= p[i-1]
            elif c2 >= p[i-1] and dp[i][c1][c2] == dp[i-1][c1][c2 - p[i-1]] + b[i-1]:
                items_in_knapsack2.append(i-1)
                c2 -= p[i-1]

    return items_in_knapsack1, items_in_knapsack2

# Ejemplo
n = 4
M1 = 5
M2 = 6
p = [2, 3, 4, 1]
b = [3, 4, 5, 6]

dp, max_benefit = two_knapsacks(n, M1, M2, p, b)
items_in_knapsack1, items_in_knapsack2 = find_items(dp, n, M1, M2, p, b)

print(f"Beneficio máximo: {max_benefit}")
print(f"Objetos en la mochila 1: {items_in_knapsack1}")
print(f"Objetos en la mochila 2: {items_in_knapsack2}")
