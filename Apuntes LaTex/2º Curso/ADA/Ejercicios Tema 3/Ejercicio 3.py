def es_valido(x, y, M, n, visitado):
    """
    Verifica si la posición (x, y) es válida para moverse.
    - x, y: Coordenadas actuales.
    - M: Matriz del laberinto.
    - n: Tamaño de la matriz.
    - visitado: Matriz que guarda las posiciones ya visitadas.
    """
    return 0 <= x < n and 0 <= y < n and M[x][y] == 'A' and not visitado[x][y]

def backtracking_laberinto(x, y, M, n, visitado, camino):
    """
    Aplica backtracking para encontrar un camino en el laberinto.
    - x, y: Posición actual.
    - M: Matriz del laberinto.
    - n: Tamaño de la matriz.
    - visitado: Matriz que guarda las posiciones ya visitadas.
    - camino: Lista que almacena el camino recorrido.
    """
    # Caso base: si llegamos a la posición final (n-1, n-1)
    if x == n - 1 and y == n - 1:
        camino.append((x, y))
        return True

    # Añadir la posición actual al camino y marcar como visitada
    camino.append((x, y))
    visitado[x][y] = True

    # Definir los 4 movimientos posibles: abajo, derecha, arriba, izquierda
    movimientos = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # Probar todos los movimientos posibles
    for dx, dy in movimientos:
        nuevo_x, nuevo_y = x + dx, y + dy
        if es_valido(nuevo_x, nuevo_y, M, n, visitado):
            if backtracking_laberinto(nuevo_x, nuevo_y, M, n, visitado, camino):
                return True

    # Backtrack: desmarcar la posición y eliminarla del camino
    visitado[x][y] = False
    camino.pop()
    return False

def resolver_laberinto(M, n):
    """
    Resuelve el problema del laberinto usando backtracking.
    - M: Matriz del laberinto.
    - n: Tamaño de la matriz.
    """
    visitado = [[False for _ in range(n)] for _ in range(n)]  # Matriz de posiciones visitadas
    camino = []  # Lista para almacenar el camino

    if backtracking_laberinto(0, 0, M, n, visitado, camino):
        print("Camino encontrado:")
        for paso in camino:
            print(paso)
    else:
        print("No se encontró un camino válido.")

# Ejemplo de uso
if __name__ == "__main__":
    M = [
        ['A', 'C', 'A', 'A'],
        ['A', 'A', 'A', 'C'],
        ['A', 'C', 'A', 'A'],
        ['C', 'A', 'A', 'A']
    ]
    n = len(M)
    resolver_laberinto(M, n)