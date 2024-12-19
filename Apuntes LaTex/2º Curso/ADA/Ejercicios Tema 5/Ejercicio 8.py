def balanced_partition(weights):
    n = len(weights)
    total_sum = sum(weights)
    half_sum = total_sum // 2

    # Inicializar tabla dp
    dp = [[False] * (half_sum + 1) for _ in range(n + 1)]
    dp[0][0] = True

    # Llenar la tabla dp
    for i in range(1, n + 1):
        for w in range(half_sum + 1):
            # Si no tomamos el objeto i-1
            dp[i][w] = dp[i-1][w]
            # Si tomamos el objeto i-1
            if w >= weights[i-1]:
                dp[i][w] = dp[i][w] or dp[i-1][w - weights[i-1]]

    # Encontrar la mayor suma posible cercana a half_sum
    for w in range(half_sum, -1, -1):
        if dp[n][w]:
            sum1 = w
            break

    sum2 = total_sum - sum1
    return abs(sum2- sum1), sum1, sum2

# Ejemplo
weights = [2, 1, 3, 4]
difference, sum1, sum2 = balanced_partition(weights)
print(f"Diferencia mínima: {difference}")
print(f"Montón 1: {sum1}, Montón 2: {sum2}")
