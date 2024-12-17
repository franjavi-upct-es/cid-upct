def es_valido(v, grafo, camino, pos):
    """
    Verifica si el vértice v puede añadirse al camino actual

    :param v: Vértice actual.
    :param grafo: Matriz de adyacencia que representa el grafo.
    :param camino: Lista con el camino actual.
    :param pos: Posición actual en el camino.
    """
    # Verifica si existe una arista desde el último vértice al vértice actual
    if not grafo[camino[pos - 1]][v]:
        return False

    # Verifica si el vértice ya ha sido visitado
    if v in camino:
        return False

    return True

def backtracking_hamiltoniano(grafo, camino, pos, n):
    """
    Aplica backtracking para encontrar un ciclo hamiltoniano

    :param grafo: Matriz de adyacencia.
    :param camino: Lista con el camino actual.
    :param pos: Posición actual en el camino.
    :param n: Número de vértices en el grafo.
    """
    # Caso base: si todos los vértices están en el camino
    if pos == n:
        # Verifica si existe un arista entre el último y el primer vértice
        if grafo[camino[pos - 1]][camino[0]]:
            return True
        else:
            return False

    # Prueba a añadir vértices al camino
    for v in range(1, n):
        if es_valido(v, grafo, camino, pos):
            camino[pos] = v # Añade el vértice al camino

            if backtracking_hamiltoniano(grafo, camino, pos + 1, n):
                return True

            # Backtrack: elimina el vértice del camino
            camino[pos] = -1

    return False

def encontrar_ciclo_hamiltoniano(grafo, n):
    """
    Resuelve el problema del ciclo hamiltoniano.

    :param grafo: Matriz de adyacencia.
    :param n: Número de vértices en el grafo.
    """
    camino = [-1] * n # Inicializa el camino
    camino[0] = 0 # Comienza en el vértice 0

    if backtracking_hamiltoniano(grafo, camino, 1, n):
        print("Ciclo Hamiltoniano encontrado:")
        print(camino + [camino[0]]) # Muestra el ciclo completo
    else:
        print("Ciclo Hamiltoniano no encontrado")

# Ejemplo de uso:
if __name__ == "__main__":
    n = 5 # Número de vértices
    grafo = [
        [0,1,0,1,0],
        [1,0,1,1,1],
        [0,1,0,0,1],
        [1,1,0,0,1],
        [0,1,1,1,0]
    ]

    encontrar_ciclo_hamiltoniano(grafo, n)