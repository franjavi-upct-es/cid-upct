def encontrar_indice_uno(T, inicio, fin):
    """
    Encuentra un índice i tal que T[i] = 1 en un arreglo ordenado.
    - T: Arreglo ordenado de enteros.
    - inicio: índice inicial de la región a buscar.
    - fin: índice final de la región a buscar.
    Retorna el índice i si existe, o -1 si no encuentra.
    """
    if inicio > fin:
        return -1 # No se encuentra el elemento

    mid = (inicio + fin) // 2 # Índice medio

    if T[mid] == 1:
        return mid # Elemento encontrado
    elif T[mid] > 1:
        return encontrar_indice_uno(T, inicio, mid - 1) # Buscar en la mitad izquierda
    else:
        return encontrar_indice_uno(T, mid + 1, fin) # Buscar en la mitad derecha

def buscar_uno(T):
    """
    Función principal para encontrar el índice de T[i] = 1 en un arreglo ordenado.
    - T: Arreglo ordenado de enteros.
    Retorna el índice si existe, o -1 si no se encuentra.
    """
    return encontrar_indice_uno(T, 0, len(T) - 1)

# Ejemplo de uso
if __name__ == '__main__':
    T = [-10, -5, -2, 0, 1, 3, 5, 8] # Arreglo de ejemplo
    indice = buscar_uno(T)
    if indice != -1:
        print(f"El índice donde T[i] = 1 es: {indice}")
    else:
        print("No se encontró ningún índice donde T[i] = 1.")
