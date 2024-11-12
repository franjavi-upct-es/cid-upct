import os
import numpy as np


def encontrar_archivos_in(directorio='.'):
    """
    Encuentra todos los archivos con extensión '.in' en el directorio especificado.

    :param directorio: Ruta del directorio donde buscar archivos. Por defecto, es el directorio actual.
    :return: Una lista de rutas de archivos que terminan en '.in' dentro del directorio especificado.
    """
    return [os.path.join(directorio, f) for f in os.listdir(directorio) if f.endswith('.in')]



def leer_entrada(file_path):
    """
    Lee un archivo de entrada y organiza los casos de prueba. Cada caso de prueba contiene:
    - El número de mecánicos (M)
    - El número de averías (A)
    - Una matriz de capacidades, donde cada fila representa un mecánico y cada columna una avería.
      Un valor de 1 en la matriz indica que el mecánico puede reparar la avería en esa posición.

    :param file_path: Ruta del archivo de entrada.
    :return: Un par de valores (P, casos), donde:
             - P es el número total de casos de prueba en el archivo.
             - casos es una lista de diccionarios, donde cada diccionario representa un caso con los
               campos 'M', 'A', y 'capacidades'.
    """
    with open(file_path, 'r') as file:
        lineas = file.readlines()
        P = int(lineas[0].strip())
        casos = []
        indice = 1
        for _ in range(P):
            M, A = map(int, lineas[indice].split())
            indice += 1
            capacidades = [list(map(int, lineas[indice + i].split())) for i in range(M)]
            casos.append({'M': M, 'A': A, 'capacidades': capacidades})
            indice += M
    return P, casos


def generar(nivel, s, M, capacidades, mecanicos_usados):
    """
    Genera una asignación de mecánico para una avería específica.

    :param nivel: Nivel actual del árbol de decisión (corresponde a la avería).
    :param s: Lista de asignaciones actuales.
    :param M: Número de mecánicos.
    :param capacidades: Matriz de capacidades de los mecánicos.
    :param mecanicos_usados: Lista de mecánicos ya asignados
    :return: Lista de asignaciones actualizada
    """
    for mecanico in range(1, M + 1):
        if (0 <= mecanico - 1 < len(capacidades)) and (0 <= nivel - 1 < len(capacidades[0])):
            if not mecanicos_usados[mecanico - 1] and capacidades[mecanico - 1][nivel - 1] == 1:
                s[nivel - 1] = mecanico
                mecanicos_usados[mecanico - 1] = True
                return s
    return s



def solucion(nivel, A):
    """
    Verifica si se ha encontrado una solución completa.

    :param nivel: Nivel actual del árbol de decisión.
    :param A: Número de averías.
    :return: True si se ha alcanzado una solución completa, False en caso contrario.
    """
    return nivel == A + 1

def criterio(nivel, s, mejor_reparadas, soluciones):
    """
    Evalúa si la solución actual es mejor que la solución registrada.

    :param nivel: Nivel actual del árbol de decisión.
    :param s: Lista de asignaciones actuales.
    :param mejor_reparadas: Número máximo de averías reparadas registrado.
    :param soluciones: Lista con la mejor solución encontrada.
    :return: True siempre, para continuar con el proceso de búsqueda.
    """
    reparadas_actuales = sum(1 for x in s if x > 0)
    if reparadas_actuales > mejor_reparadas[0]:
        mejor_reparadas[0] = reparadas_actuales
        soluciones[:] = s.copy()
    return True



def masHermanos(nivel, s, M, capacidades, mecanicos_usados):
    """
    Determina si existen más mecánicos que pueden ser asignados a una avería en el nivel actual.

    :param nivel: Nivel actual del árbol de decisión.
    :param s: Lista de asignaciones actuales.
    :param M: Número de mecánicos.
    :param capacidades: Matriz de capacidades de los mecánicos.
    :param mecanicos_usados: Lista de mecánicos ya asignados.
    :return: True si hay más mecánicos disponibles, False en caso contrario.
    """
    mecanico_actual = s[nivel - 1]
    for mecanico in range(mecanico_actual + 1, M + 1):
        if not mecanicos_usados[mecanico - 1] and capacidades[mecanico - 1][nivel - 1] == 1:
            return True
    return False



def retroceder(nivel, s, mecanicos_usados):
    """
    Retrocede un nivel en el árbol de decisiones deshaciendo asignación de un mecánico.

    :param nivel: Nivel actual del árbol de decisión.
    :param s: Lista de asignaciones actuales.
    :param mecanicos_usados: Lista de mecánicos ya asignados.
    :return: Lista de mecánicos actualizada después del retroceso.
    """
    mecanico_actual = s[nivel - 1]
    if mecanico_actual > 0:
        mecanicos_usados[mecanico_actual - 1] = False
    s[nivel - 1] = 0
    return s



def backtracking(s_inicial, M, A, capacidades, mejor_reparadas, soluciones):
    """
    Implementa el algoritmo de backtracking para encontrar la asignación óptima de mecánicos a averías.

    :param s_inicial: Lista inicial de asignaciones (inicialmente vacía).
    :param M: Número de mecánicos.
    :param A: Número de averías.
    :param capacidades: Matriz de capacidades de los mecánicos.
    :param mejor_reparadas: Lista que almacena el número máximo de averías reparadas.
    :param soluciones: Lista que almacena la mejor solución encontrada.
    :return: Lista de asignaciones óptima.
    """
    nivel = 1
    s = s_inicial
    mecanicos_usados = [False] * M
    fin = False
    while not fin and nivel != 0:
        s = generar(nivel, s, M, capacidades, mecanicos_usados)
        if solucion(nivel, A):
            fin = True
        elif criterio(nivel, s, mejor_reparadas, soluciones):
            nivel += 1
        else:
            while not masHermanos(nivel, s, M, capacidades, mecanicos_usados) and nivel > 0:
                s = retroceder(nivel, s, mecanicos_usados)
                nivel -= 1
    return s



def backtracking_todas(M, A, capacidades):
    """
    Encuentra la mejor solución posible utilizando el algoritmo de backtracking.

    :param M: Número de mecánicos.
    :param A: Número de averías.
    :param capacidades: Matriz de capacidades de los mecánicos.
    :return: Número máximo de averías reparadas y la lista de asignaciones correspondiente.
    """
    soluciones = [0] * A
    mejor_reparadas = [0]
    s_inicial = [0] * A
    backtracking(s_inicial, M, A, capacidades, mejor_reparadas, soluciones)
    return mejor_reparadas[0], soluciones



def solution_todas(P, casos):
    """
    Procesa todos los casos de prueba y obtiene las soluciones óptimas para cada uno,
    utilizando el algoritmo de backtracking adaptado.

    :param P: Número de casos de prueba.
    :param casos: Lista de casos de prueba, donde cada caso es un diccionario con los siguientes datos:
                  - 'M': Número de mecánicos
                  - 'A': Número de averías
                  - 'capacidades': Matriz de capacidades de los mecánicos
    :return: Un string formateado que contiene las soluciones para cada caso de prueba en el formato:
             "{P}\n{reparadas}\n{asignaciones}\n...", donde "reparadas" es el número de averías reparadas
             y "asignaciones" es la lista de asignaciones de mecánicos.
    """
    resultados = []
    for caso in casos:
        M, A, capacidades = caso['M'], caso['A'], np.array(caso['capacidades'])
        max_reparadas, solucion = backtracking_todas(M, A, capacidades)
        resultado = f"{max_reparadas}\n{' '.join(map(str, solucion))}"
        resultados.append(resultado)

    return f"{P}\n" + "\n".join(resultados)


if __name__ == '__main__':
    file_paths_in = encontrar_archivos_in('.')

    for file_path in file_paths_in:
        P, casos = leer_entrada(file_path)
        resultados = solution_todas(P, casos)
    
        print(resultados)
        print()
