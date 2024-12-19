import numpy as np


def flight_schedule(T, E):
    """
    Resuelve el problema de planificación de vuelos con programación dinámica.

    :param T: Matriz de tiempos directos entre ciudades (np.array).
    :param E: Tiempo de escala adicional entre ciudades (np.array).
    :return: Matriz dp con tiempos mínimos y matriz next para reconstruir las rutas.
    """
    n = len(T)
    # Inicializar las matrices de DP y next
    dp = np.full((n, n), float('inf'))  # dp[i][j] almacena el tiempo mínimo de i a j
    next_city = [[-1 for _ in range(n)] for _ in range(n)]  # Para reconstruir rutas

    # Condiciones iniciales: tiempos directos de T
    for i in range(n):
        for j in range(n):
            if i != j:  # No hay bucles en sí mismos
                dp[i][j] = T[i][j] if T[i][j] != -1 else float('inf')
                if T[i][j] != -1:  # Si hay un vuelo directo
                    next_city[i][j] = j  # La siguiente ciudad en la ruta es directamente j

    # Aplicar la fórmula de DP considerando ciudades intermedias
    for k in range(n):  # Consideramos cada ciudad como intermedia
        for i in range(n):
            for j in range(n):
                # Actualizar el tiempo mínimo si pasar por k mejora la ruta
                if dp[i][k] + E[i][k][j] + dp[k][j] < dp[i][j]:
                    dp[i][j] = dp[i][k] + E[i][k][j] + dp[k][j]
                    next_city[i][j] = next_city[i][k]  # Actualizamos la ciudad siguiente

    return dp, next_city


def reconstruct_path(next_city, start, end):
    """
    Reconstruye la ruta óptima de start a end usando la matriz next_city.

    :param next_city: Matriz para reconstruir rutas (lista de listas).
    :param start: Ciudad de inicio.
    :param end: Ciudad de destino.
    :return: Lista con la secuencia de ciudades de la ruta óptima.
    """
    n = len(next_city)  # Número de ciudades
    if start < 0 or start >= n or end < 0 or end >= n:  # Validación de índices
        raise ValueError(f"Indices fuera de rango: start={start}, end={end}")

    if next_city[start][end] == -1:  # Si no hay ruta disponible
        return []
    path = [start]  # Inicializamos la ruta con la ciudad de inicio
    while start != end:  # Mientras no lleguemos al destino
        start = next_city[start][end]  # Avanzamos a la siguiente ciudad
        if start == -1:  # Verificación adicional para evitar errores
            return []
        path.append(start)  # Añadimos la ciudad actual al camino
    return path


# Ejemplo de uso:
T = np.array([
    [-1, 2, 1, 3],  # Tiempos de vuelo desde A
    [2, -1, -1, 1],  # Tiempos de vuelo desde B
    [3, 4, 8, -1]  # Tiempos de vuelo desde D
])

# Matriz de tiempos de escala (suponemos escala de 1 para todas las combinaciones)
n = len(T)
E = np.full((n, n, n), 1)  # Escalas constantes de 1 para simplificar

# Resolver el problema
dp, next_city = flight_schedule(T, E)

# Mostrar resultados
print("Matriz de tiempos mínimos (dp):")
print(dp)
print("\nMatriz next_city:")
print(next_city)

# Reconstruir ruta óptima de A (0) a D (2)
start, end = 0, 2 # Corregido el índice de destino para evitar errores
route = reconstruct_path(next_city, start, end)
print(f"\nRuta óptima de {start} a {end}: {route}")
