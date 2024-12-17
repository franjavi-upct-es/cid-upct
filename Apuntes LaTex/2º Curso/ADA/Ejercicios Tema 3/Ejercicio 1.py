def es_valido(nodo, color, solucion, A, n):
    """
    Verifica si el color asignado al nodo es válido.
    - nodo: El nodo actual
    - color: Color que se intenta asignar al nodo.
    - solucion: Lista de colores asignados hasta el momento.
    - A: Matriz de adyacencia.
    - n: Número nodos en el grafo.
    """
    for vecino in range(n):
        if A[nodo][vecino] and solucion[vecino] == color:  # Verifica adyacencia y conflicto de colores
            return False
    return True

def backtracking(nodo, A, n, max_color, solucion):
    """
    Aplica backtracking para asignar colores a los nodos.
    - nodo: Nodo actual a colorear
    - A: Matriz de adyacencia.
    - n: Número de nodos.
    - max_color: Número máximo de colores permitidos.
    - solucion: Lista con los colores asignados.
    """
    if nodo == n: # Caso base: Todos los nodos han sido coloreados
        return True

    for color in range(1, max_color + 1): # Intenta con todos los colores posibles
        if es_valido(nodo, color, solucion, A, n):
            solucion[nodo] = color # Asigna el color

            if backtracking(nodo + 1, A, n, max_color, solucion): # Llamada recursiva
                return True

            solucion[nodo] = 0 # Backtracking: Desasignar el color

    return False

def solucionar_coloreo(A, n, max_color):
    """
    Resuelve el problema de coloración de grafos.
    - A: Matriz de adyacencia.
    - n: Número de nodos.
    - max_color: Número máximo de colores permitidos.
    """
    solucion = [0] * n # Inicializar solución vacía
    if backtracking(0, A, n, max_color, solucion):
        print("Solución encontrada:")
        print(solucion)

# Ejemplo de uso:
if __name__ == '__main__':
    n = 4 # Número de nodos
    A = [
        [False, True, True, True],
        [True, False, True, False],
        [True, True, False, True],
        [True, False, True, False]
    ]
    max_color = 3 # Número máximo de colores permitidos

    solucionar_coloreo(A, n, max_color)

