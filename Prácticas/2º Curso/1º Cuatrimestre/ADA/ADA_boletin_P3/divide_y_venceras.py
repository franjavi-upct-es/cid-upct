def resolver_directo(A, m, C):
    """
    Encuentra la subcadena óptima utilizando un método directo

    :param A: Cadena original (str)
    :param m: Longitud de la cadena (int)
    :param C: Carácter a buscar (str)
    :return: tuple: Índice de inicio de la subcadena óptima y el número máximo de apariciones consecutivas.
    """
    n = len(A)
    max_consecutivos = 0
    inicio_optimo = -1

    # Recorrer todas las subcadenas de longitud m
    for i in range(n - m + 1):
        subcadena = A[i:i + m]

        # Contar el número máximo de apariciones consecutivas de C en la subcadena
        contador_actual = 0
        max_actual = 0

        for char in subcadena:
            if char == C:
                contador_actual += 1
                if contador_actual > max_actual:
                    max_actual = contador_actual
            else:
                contador_actual = 0

        # Actualizar la mejor solución encontrada
        if max_actual > max_consecutivos:
            max_consecutivos = max_actual
            inicio_optimo = i

    return inicio_optimo, max_consecutivos


def divide_y_venceras(A, m, C, l, r):
    """
    Esquema recursivo del algoritmo divide y vencerás.

    :param A: Cadena original (str)
    :param m: Longitud de la subcadena (int)
    :param C: Carácter a buscar (str)
    :param l: Índice izquierdo del rango actual (int)
    :param r: Índice derecho del rango actual (int)
    :return: tuple: Índice de inicio de la subcadena óptima y el número máximo de apariciones consecutivas.
    """
    if r - l + 1 <= m:
        return resolver_directo(A[l:r + 1], m, C)

    mid = (l + r) // 2

    # Soluciones para las dos mitades
    sol_izq = divide_y_venceras(A, m, C, l, mid)
    sol_der = divide_y_venceras(A, m, C, mid + 1, r)

    # Solución que cruza el centro
    max_central_consecutivos = 0
    inicio_central = -1

    # Buscar subcadena que cruce el centro
    for i in range(mid - m + 1, mid + 1):
        if i < l or i + m - 1 > r:
            continue
        subcadena = A[i:i + m]
        contador_actual = 0
        max_actual = 0

        for char in subcadena:
            if char == C:
                contador_actual += 1
                max_actual = max(max_actual, contador_actual)
            else:
                contador_actual = 0

        if max_actual > max_central_consecutivos:
            max_central_consecutivos = max_actual
            inicio_central = i

    sol_central = (inicio_central, max_central_consecutivos)

    return max(sol_izq, sol_der, sol_central, key=lambda x: x[1])

if __name__ == '__main__':
    # Ejemplo de uso
    import random

    # Generar una cadena de ejemplo con el alfabeto
    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    C = 'c'  # Carácter a buscar
    m = 100  # Tamaño de la subcadena fijo
    num_pruebas = 5 # Número de pruebas a realizar para comprobar que el código funciona

    for i in range(num_pruebas):
        print(f"\n -- Prueba {i + 1} --")
        A = ''.join(random.choices(alfabeto, k=1000))  # Cadena aleatoria de longitud 1000
        resultado = divide_y_venceras(A, m, C, 0, len(A) - 1)
        print(f"Índice de inicio: {resultado[0]} \nMáximo de apariciones consecutivas: {resultado[1]}")
