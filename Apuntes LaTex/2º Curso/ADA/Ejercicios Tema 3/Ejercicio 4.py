import math

def es_valido(asignados, arbitro, partido, partidos, P):
    """
    Verifica si un árbitro puede ser asignado al partido actual.
    - asignados: Lista de árbitros asignados hasta ahora.
    - arbitro: Árbitro actual a evaluar.
    - partido: Índice del partido actual.
    - partidos: Lista de partidos con equipos enfrentados.
    - P: Matriz de puntuaciones de preferencias.
    """
    equipo1, equipo2 = partidos[partido]  # Equipos en el partido actual
    # Verificar si el árbitro ya fue asignado
    if arbitro in asignados:
        return False
    # Verificar que la preferencia no sea -infinito para ninguno de los equipos
    if P[equipo1][arbitro] == -math.inf or P[equipo2][arbitro] == -math.inf:
        return False
    return True

def backtracking_arbitros(partido, asignados, puntuacion_actual, max_puntuacion, partidos, P, solucion_actual,
                          mejor_solucion):
    """
    Aplica backtracking para asignar árbitros a partidos.
    - partido: Índice del partido actual.
    - asignados: Lista de árbitros ya asignados.
    - puntuacion_actual: Puntuación total de la asignación actual.
    - max_puntuacion: Valor máximo de la puntuación encontrada hasta ahora.
    - partidos: Lista de partidos con equipos enfrentados.
    - P: Matriz de puntuaciones de preferencias.
    - solucion_actual: Lista con la asignación actual.
    - mejor_solucion: Lista con la mejor asignación encontrada.
    """
    # Caso base: Se asignaron árbitros a todos los partidos
    if partido == len(partidos):
        if puntuacion_actual > max_puntuacion[0]:
            max_puntuacion[0] = puntuacion_actual
            mejor_solucion[:] = solucion_actual[:]
        return

    # Probar asignar cada árbitro disponible
    for arbitro in range(len(P[0])):
        if es_valido(asignados, arbitro, partido, partidos, P):
            # Actualizar asignación y puntuación
            equipo1, equipo2 = partidos[partido]
            nueva_puntuacion = puntuacion_actual + P[equipo1][arbitro] + P[equipo2][arbitro]
            asignados.append(arbitro)
            solucion_actual.append(arbitro)

            # Llamada recursiva al siguiente partido
            backtracking_arbitros(partido + 1, asignados, nueva_puntuacion, max_puntuacion, partidos, P,
                                  solucion_actual, mejor_solucion)

            # Backtrack: deshacer cambios
            asignados.pop()
            solucion_actual.pop()

def asignar_arbitros(n, m, P, partidos):
    """
    Encuentra la asignación óptima de árbitros para los partidos usando backtracking.
    - n: Número de equipos.
    - m: Número de árbitros.
    - P: Matriz de puntuaciones de preferencias.
    - partidos: Lista de partidos con equipos enfrentados.
    """
    max_puntuacion = [-math.inf]  # Puntuación máxima encontrada
    mejor_solucion = []  # Mejor asignación encontrada
    asignados = []  # Árbitros ya asignados
    solucion_actual = []  # Asignación actual

    backtracking_arbitros(0, asignados, 0, max_puntuacion, partidos, P, solucion_actual, mejor_solucion)

    print("Mejor puntuación total:", max_puntuacion[0])
    print("Asignación de árbitros a partidos:", mejor_solucion)

# Ejemplo de uso
if __name__ == "__main__":
    n = 4  # Número de equipos
    m = 3  # Número de árbitros
    P = [  # Matriz de preferencias
        [8, -math.inf, 7],
        [6, 9, -math.inf],
        [-math.inf, 7, 8],
        [7, 8, -math.inf]
    ]
    partidos = [(0, 1), (2, 3)]  # Lista de partidos (equipos enfrentados)
    asignar_arbitros(n, m, P, partidos)
