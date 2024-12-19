def maximize_utility(K, products):
    """
    Maximiza la utilidad de los productos comprados con un presupuesto dado.

    :param K: Presupuesto disponible.
    :param products: Lista de productos, cada uno con (precio, utilidad).
    :return: Máxima utilidad y lista de productos comprados.
    """
    # Número de productos
    m = len(products)

    # Tabla DP para almacenar la utilidad máxima para cada presupuesto
    dp = [0] * (K + 1)
    # Tabla para reconstrucción de solución
    decisions = [[0] * (K + 1) for _ in range(m)]

    # Iterar sobre cada producto
    for i, (p, u) in enumerate(products):
        # Iterar sobre el presupuesto en orden inverso
        for j in range(K, -1, -1):
            # Opción 1: Comprar 1 unidad
            if j >= p:
                if dp[j] < dp[j - p] + u:
                    dp[j] = dp[j - p] + u
                    decisions[i][j] = 1
            # Opción 2: Comprar 2 unidades
            if j >= 2 * p - 1:
                if dp[j] < dp[j - (2 * p - 1)] + 2 * u:
                    dp[j] = dp[j - (2 * p - 1)] + 2 * u
                    decisions[i][j] = 2
            # Opción 3: Comprar 3 unidades
            if j >= 3 * p - 3:
                if dp[j] < dp[j - (3 * p - 3)] + 3 * u:
                    dp[j] = dp[j - (3 * p - 3)] + 3 * u
                    decisions[i][j] = 3

 	# Reconstruir la solución
 	j = K
 	solution = [0] * m
 	for i in range(m - 1, -1, -1):
 		solution[i] = decisions[i][j]
		if solution[i] == 1:
          j -= products[i][0]
      elif solution[i] == 2:
          j -= (2 * products[i][0] - 1)
      elif solution[i] == 3:
          j -= (3 * products[i][0] - 3)

	return dp[K], solution

# Ejemplo de uso
K = 10
products = [
    (3, 4), # Producto 1: precio base 3, utilidad 4
    (5, 7), # Producto 2: precio base 5, utilidad 7
]

max_utility, solution = maximize_utility(K, products)
print(f"Máxima utilidad: {max_utility}")
print(f"Productos comprados (unidades por producto): {solution}")

