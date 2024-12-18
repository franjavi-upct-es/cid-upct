def find_all_solutions(dp, weights, values, n, W):
    solutions = []

    def bactrack(i, w, current_solution):
        if i == 0 or w == 0:
            solutions.append(current_solution[:])
            return

        # Caso donde el elemento no está  incluido
