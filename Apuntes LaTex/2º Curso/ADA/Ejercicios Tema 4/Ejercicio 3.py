def suma_maxima_cruzada(arr, inicio, medio, fin, n):
    """
    Calcula la suma máxima de una subcadena de longitud n que cruza el punto medio del arreglo.
    - arr: Arreglo de enteros.
    - inicio: índice de inicio del intervalo.
    - medio: índice medio del intervalo.
    - fin: índice final del intervalo.
    - n: Longitud de la subcadena buscada.
    Retorna la suma máxima encontrada.
    """
    max_izquierda = float('-inf')
    suma_actual = 0

    # Considerar las subcadenas del lado izquierdo que terminan en medio
    for i in range(medio, max(inicio, medio - n + 1) - 1, -1):
        suma_actual += arr[i]
        max_izquierda = max(max_izquierda, suma_actual) if medio - i + 1 <= n else max_izquierda

    max_derecha = float('-inf')
    suma_actual = 0

    # Considerar las subcadenas del lado derecho que comienzan en medio + 1
    for i in range(medio + 1, min(fin + 1, medio + n + 1)):
        suma_actual += arr[i]
        max_derecha = max(max_derecha, suma_actual) if i - medio <= n else max_derecha

    return max_izquierda + max_derecha


def suma_maxima_dyv(arr, inicio, fin, n):
    """
    Divide y vence para encontrar la suma máxima de una subcadena de longitud n.
    - arr: Arreglo de enteros.
    - inicio: índice de inicio del intervalo.
    - fin: índice final del intervalo.
    - n: Longitud de la subcadena buscada.
    Retorna la suma máxima encontrada.
    """
    # Caso base: Si el intervalo es exactamente de longitud n
    if fin - inicio + 1 == n:
        return sum(arr[inicio:inicio + n])

    if fin - inicio + 1 < n:
        return float('-inf')

    # Dividir el arreglo en dos mitades
    medio = (inicio + fin) // 2

    # Resolver las subcadenas máximas en las dos mitades
    suma_izquierda = suma_maxima_dyv(arr, inicio, medio, n)
    suma_derecha = suma_maxima_dyv(arr, medio + 1, fin, n)

    # Resolver la subcadena máxima que cruza el punto medio
    suma_cruzada = suma_maxima_cruzada(arr, inicio, medio, fin, n)

    # Retornar la máxima de las tres
    return max(suma_izquierda, suma_derecha, suma_cruzada)


def buscar_suma_maxima(arr, n):
    """
    Función principal para encontrar la subcadena de longitud n con suma máxima.
    - arr: Arreglo de enteros.
    - n: Longitud de la subcadena buscada.
    Retorna la suma máxima encontrada.
    """
    if len(arr) < n:
        raise ValueError("La longitud de la subcadena no puede ser mayor que el tamaño del arreglo.")
    return suma_maxima_dyv(arr, 0, len(arr) - 1, n)

# Ejemplo de uso
if __name__ == "__main__":
    arr = [2, -1, 3, 5, -2, 8, -1, 4]
    n = 3
    resultado = buscar_suma_maxima(arr, n)
    print(f"La suma máxima de una subcadena de longitud {n} es: {resultado}")
