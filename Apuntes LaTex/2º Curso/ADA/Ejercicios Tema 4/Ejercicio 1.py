def encontrar_mayores(arr):
    """
    Encuentra el mayor y el segundo mayor elemento de un arreglo utilizando divide y vencerás.

    - arr: Lista de enteros.
    Retorna: (mayor, segundo_mayor, comparaciones)
    """
    def dividir_y_vencer(arr):
        # Caso base: Si hay solo dos elementos, compara directamente
        if len(arr) == 2:
            if arr[0] > arr[1]:
                return arr[0], arr[1], 1 # mayor, segundo mayor, comparaciones
            else:
                return arr[1], arr[0], 1

        # Divide el arreglo en dos mitades
        mid = len(arr) // 2
        izq_mayor, izq_segundo, izq_comparaciones = dividir_y_vencer(arr[:mid])
        der_mayor, der_segundo, der_comparaciones = dividir_y_vencer(arr[mid:])

        # Combina las soluciones
        comparaciones = izq_comparaciones + der_comparaciones

        if izq_mayor > der_mayor:
            mayor = izq_mayor
            segundo_mayor = max(izq_segundo, der_mayor)
        else:
            mayor = der_mayor
            segundo_mayor = max(der_segundo, izq_mayor)

        comparaciones += 2 # Comparaciones para determinar mayor y segundo mayor
        return mayor, segundo_mayor, comparaciones

    # Llamar a la función recursiva
    return dividir_y_vencer(arr)

# Ejemplo de uso
if __name__ == '__main__':
    arr = [10, 3, 5, 7, 9, 2, 6, 8]
    mayor, segundo_mayor, comparaciones = encontrar_mayores(arr)
    print(f"Mayor elemento: {mayor}")
    print(f"Segundo mayor elemento: {segundo_mayor}")
    print(f"Total de comparaciones: {comparaciones}")
