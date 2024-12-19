def longest_increasing_subsequence(arr):
    n = len(arr)
    dp = [1] * n # dp[i] almacena la longtiud de la subsecuencia más larga que termina en arr[i]
    prev = [-1] * n # prev[i] almacena el índice del elemento anterior en la subsecuencia

    # Calcular dp[i] para todos los i
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # Encontrar la longitud máxima de la subsecuencia
    max_length = max(dp)
    max_index = dp.index(max_length)

    # Reconstruir la subsecuencia
    subsequence = []
    while max_index != -1:
        subsequence.append(arr[max_index])
        max_index = prev[max_index]
    subsequence.reverse()

    return max_length, subsequence

# Ejemplo
arr = [3, 1, 3, 2, 3, 8, 4, 7, 5, 4, 6]
length, subsequence = longest_increasing_subsequence(arr)
print(f"Longitud de la subsecuencia creciente más larga: {length}")
print(f"Subsecuencia: {subsequence}")
