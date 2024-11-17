import os
import sys

def encontrar_archivos_in(directorio='.'):
    """
    Encuentra todos los archivos con extensión '.in' en el directorio especificado, incluyendo subdirectorios.

    :param directorio: Ruta del directorio donde buscar archivos. Por defecto, es el directorio actual.
    :return: Una lista de rutas de archivos que terminan en '.in' dentro del directorio especificado.
    """
    archivos_in = []
    for root, dirs, files in os.walk(directorio):
        for f in files:
            if f.endswith('.in'):
                archivos_in.append(os.path.join(root, f))
    return archivos_in

def leer_entrada(ruta_archivo):
    """
    Lee un archivo de entrada y organiza los casos de prueba.

    :param ruta_archivo: Ruta del archivo de entrada.
    :return: Una tupla (P, casos), donde:
             - P es el número total de casos de prueba en el archivo.
             - casos es una lista de diccionarios, cada uno representando un caso con 'M', 'A' y 'capacidades'.
    """
    with open(ruta_archivo, 'r') as archivo:
        lineas = [linea.strip() for linea in archivo if linea.strip()]
        P = int(lineas[0])
        casos = []
        indice = 1
        for _ in range(P):
            M, A = map(int, lineas[indice].split())
            indice += 1
            capacidades = []
            for _ in range(M):
                capacidad = list(map(int, lineas[indice].split()))
                capacidades.append(capacidad)
                indice += 1
            casos.append({'M': M, 'A': A, 'capacidades': capacidades})
    return P, casos

def backtrack_asignar(averias, mecanicos_por_averia, asignaciones, asignaciones_mecanicos, indice, mejor, cuenta_actual):
    """
    Función de backtracking optimizada con poda para asignar averías a mecánicos.

    :param averias: Lista de averías a asignar.
    :param mecanicos_por_averia: Lista donde cada índice representa una avería y contiene la lista de mecánicos que pueden repararla.
    :param asignaciones: Lista actual de asignaciones (índice de mecánico por avería).
    :param asignaciones_mecanicos: Lista que rastrea cuántas averías ha sido asignadas a cada mecánico.
    :param indice: Índice de la avería actual a asignar.
    :param mejor: Diccionario con la mejor asignación encontrada hasta ahora.
    :param cuenta_actual: Número actual de averías asignadas.
    """
    if indice == len(averias):
        if cuenta_actual > mejor['cuenta']:
            mejor['cuenta'] = cuenta_actual
            mejor['asignacion'] = asignaciones.copy()
        return

    # Poda: si la suma de averías actuales y las que aún se pueden asignar no supera el mejor
    max_restante = len(averias) - indice
    if cuenta_actual + max_restante <= mejor['cuenta']:
        return  # No es posible mejorar el resultado actual

    averia = averias[indice]
    # Iterar sobre los mecánicos que pueden reparar esta avería, en orden ascendente para lexicografía mínima
    for mecanico in sorted(mecanicos_por_averia[averia]):
        if asignaciones_mecanicos[mecanico] == 0:
            # Asignar avería al mecánico
            asignaciones[indice] = mecanico
            asignaciones_mecanicos[mecanico] += 1

            # Actualizar cuenta_actual
            nueva_cuenta = cuenta_actual + 1

            # Recurser para la siguiente avería
            backtrack_asignar(averias, mecanicos_por_averia, asignaciones, asignaciones_mecanicos, indice + 1, mejor, nueva_cuenta)

            # Deshacer la asignación
            asignaciones_mecanicos[mecanico] -= 1
            asignaciones[indice] = 0

    # Opción de no asignar ninguna avería al mecánico actual (0)
    # Solo si es preferible dejarla sin asignar
    # Para asegurar que los 0's queden al final, realizamos esta asignación después de intentar asignar a mecánicos
    backtrack_asignar(averias, mecanicos_por_averia, asignaciones, asignaciones_mecanicos, indice + 1, mejor, cuenta_actual)

def backtracking_maximo(M, A, capacidades):
    """
    Calcula la asignación óptima de averías a mecánicos utilizando backtracking.

    :param M: Número de mecánicos.
    :param A: Número de averías.
    :param capacidades: Matriz de capacidades de los mecánicos.
    :return: Tupla (número de averías reparadas, lista de asignaciones por avería)
    """
    # Convertir capacidades a una lista donde cada avería tiene los mecánicos que pueden repararla
    # Índice 1 a A
    mecanicos_por_averia = [[] for _ in range(A + 1)]  # 1-based
    for mecanico in range(1, M + 1):
        for averia in range(1, A + 1):
            if capacidades[mecanico - 1][averia - 1] == 1:
                mecanicos_por_averia[averia].append(mecanico)

    averias = list(range(1, A + 1))
    # Ordenar averías por el número de mecánicos que pueden repararlas (ascendente) para optimizar la poda
    averias.sort(key=lambda x: len(mecanicos_por_averia[x]))
    asignaciones = [0] * A  # 0 indica sin asignación
    mejor = {'cuenta': 0, 'asignacion': asignaciones.copy()}

    # Asignaciones por mecánico (sin límite, pero cada mecánico solo puede tener una asignación)
    asignaciones_mecanicos = [0] * (M + 1)  # 1-based

    backtrack_asignar(averias, mecanicos_por_averia, asignaciones, asignaciones_mecanicos, 0, mejor, 0)

    return mejor['cuenta'], mejor['asignacion']

def procesar_todos(P, casos):
    """
    Procesa todos los casos de prueba y obtiene las soluciones óptimas para cada uno,
    utilizando el algoritmo de backtracking.

    :param P: Número de casos de prueba.
    :param casos: Lista de casos de prueba, cada uno es un diccionario con 'M', 'A' y 'capacidades'.
    :return: Una cadena formateada con las soluciones para cada caso de prueba.
    """
    resultados = []
    for caso in casos:
        M = caso['M']
        A = caso['A']
        capacidades = caso['capacidades']
        reparadas, asignacion = backtracking_maximo(M, A, capacidades)
        # Asegurar que la lista de asignaciones tenga exactamente A valores
        # No es necesario rellenar con 0, ya que se maneja en el backtracking
        asignacion_str = ' '.join(map(str, asignacion))
        resultados.append(f"{reparadas}\n{asignacion_str}")
    salida = f"{P}\n" + "\n".join(resultados)
    return salida

if __name__ == '__main__':
    directorio = os.path.dirname(__file__) if '__file__' in globals() else '.'
    archivos_in = encontrar_archivos_in(directorio)

    if not archivos_in:
        print(f"No se encontraron archivos con extensión '.in' en el directorio '{directorio}'.")
        sys.exit()

    for ruta_archivo in archivos_in:
        ruta_relativa = os.path.relpath(ruta_archivo, directorio)
        print(f"Procesando archivo: '{ruta_relativa}'")
        P, casos = leer_entrada(ruta_archivo)
        if P > 0:
            resultado = procesar_todos(P, casos)
            print(resultado)
            print()
        else:
            print("No se procesaron casos de prueba.\n")