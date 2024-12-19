def find_all_solutions(dp, weights, values, n, W):
    solutions = []

    def bactrack(i, w, current_solution):
        if i == 0 or w == 0:
            solutions.append(current_solution[:])
            return

        # Caso donde el elemento no está incluido
        if dp[i][w] == dp[i - 1][w]:
            bactrack(i-1, w, current_solution)

        # Caso donde el elemento está incluido
        if w >= weights[i-1] and dp[i][w] == dp[i - 1][w - weights[i-1]] + values[i-1]:
            current_solution.append(i-1) # Incluye el íindice del elemento
            bactrack(i-1, w - weights[i-1], current_solution)
            current_solution.pop() # Deshace la inclusión para explorar otras ramas

    bactrack(n, W, [])
    return solutions

# Verificación de unicidad:
solutions = find_all_solutions(dp, weights, values, n, W)
if len(solutions) == 1:
    print(f"La solución óptima es única {solutions[0]}")
else:
    print(f"Existen múltiples soluciones óptima: {solutions}")