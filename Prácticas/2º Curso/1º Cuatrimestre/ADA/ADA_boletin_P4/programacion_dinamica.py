import random

def construir_tabla(N, E, p, t):
    """
    Construye la tabla de programación dinámica para maximizar el número de tenedores.

    :param N: Número de bares
    :param E: Presupuesto total
    :param p: Lista de precios de cada bar (índice desde 0)
    :param t: Lista de tenedores de cada bar (índice desde 0)
    :return: Tabla dp con los valores máximos de tenedores para cada subproblema.
    """

    # Inicializar la tabla dp con ceros
    dp = [[0] * (E + 1) for _ in range(N + 1)]

    # Construcción de la tabla dp
    for i in range(1, N + 1):
        pi = p[i - 1]
        ti = t[i - 1]
        for e in range(E + 1):
            dp[i][e] = dp[i - 1][e] # No tomar tapas del bar i
            for k in range(1, 4):   # Tomar hasta 3 tapas del bar i
                coste = k * pi
                if e >= coste:
                    valor = dp[i - 1][e - coste] + k * ti
                    if valor > dp[i][e]:
                        dp[i][e] = valor
                else:
                    break   # No podemos permitirnos más tapas en este bar

    return dp

def reconstruir_solucion(N, E, p, t, dp):
    """
    Reconstruye la solución óptima a partir de la tabla dp.

    :param N: Número de bares.
    :param E: Presupuesto total.
    :param p: Lista de precios de cada bar.
    :param t: Lista de tenedores de cada bar.
    :param dp: Tabla dp construida previamente
    :return: Lista con el número de tapas tomadas en cada bar
    """
    # Inicializar la lista de tapas por bar
    tapas_por_bar = [0] * N
    e = E
    for i in range(N, 0, -1):
        if dp[i][e] != dp[i - 1][e]:
            # Tomamos alguna tapa del bar ir
            pi = p[i - 1]
            ti = t[i - 1]
            for k in range(1, 4):
                coste = k * pi
                if e >= coste and dp[i][e] == dp[i - 1][e - coste] + k * ti:
                    tapas_por_bar[i - 1] = k
                    e -= coste
                    break
    return tapas_por_bar

if __name__ == '__main__':
    for i in range(10):
        print(f"\n -- Prueba {i + 1} --")
        N = random.randint(1, 10)  # Número de bares entre 1 y 10
        E = random.randint(10, 100)  # Presupuesto entre 10 y 100
        p = [random.randint(1, 10) for _ in range(N)]  # Precios aleatorios entre 1 y 10
        t = [random.randint(1, 5) for _ in range(N)]  # Tenedores aleatorios entre 1 y 5

        dp = construir_tabla(N, E, p, t)
        tapas_por_bar = reconstruir_solucion(N, E, p, t, dp)

        print(f"Número de bares: {N}")
        print(f"Presupuesto total: {E} euros")
        print(f"Precios por bar: {p}")
        print(f"Tenedores por bar: {t}")
        print(f"Tapas por bar: {tapas_por_bar}")
        print(f"Máximo número de tenedores: {dp[N][E]}")
