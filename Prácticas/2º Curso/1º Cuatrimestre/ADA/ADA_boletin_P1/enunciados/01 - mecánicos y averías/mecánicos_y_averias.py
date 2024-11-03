import os

def encontrar_archivos_in(directorio='.'):
    """
    Busca todos los archivos .in en el directorio especificado.

    :param directorio: Ruta del directorio donde buscar archivos `.in`.
    :return: Lista de rutas de archivos `.in` encontradas.
    """
    archivos_in = []
    for root, _, files in os.walk(directorio):
        for file in files:
            if file.endswith('.in'):
                archivos_in.append(os.path.join(root, file))
    return archivos_in

def encontrar_archivos_out(directorio='.'):
    """
    Busca todos los archivos .out en el directorio especificado para hacer la validación de los resultados obtenidos.

    :param directorio: Ruta del directorio donde buscar archivos `.out`.
    :return: Lista de rutas de archivos `.out` encontradas.
    """
    archivos_in = []
    for root, _, files in os.walk(directorio):
        for file in files:
            if file.endswith('.out'):
                archivos_in.append(os.path.join(root, file))
    return archivos_in


def leer_entrada(file_path):
    """
    Lee el archivo de entrada y convierte la información en una estructura de datos adecuada.

    :param file_path: Ruta del archivo de entrada.
    :return: Número de casos de prueba (P) y lista de casos de prueba.
    """
    with open(file_path, 'r') as file:
        lineas = file.readlines()

    P = int(lineas[0].strip())
    casos = []
    indice = 1

    for _ in range(P):
        M, A = map(int, lineas[indice].strip().split())
        indice += 1

        capacidades = []
        for _ in range(M):
            capacidades.append(list(map(int, lineas[indice].strip().split())))
            indice += 1

        casos.append({'M': M, 'A': A, 'capacidades': capacidades})

    return P, casos


def factible(mecanico, averia, capacidades, asignaciones):
    """
    Verifica si un mecánico puede ser asignado a una avería.

    :param mecanico: Índice del mecánico.
    :param averia: Índice de la avería.
    :param capacidades: Matriz de capacidades de los mecánicos.
    :param asignaciones: Lista de asignaciones de averías.
    :return: True si el mecánico puede reparar la avería y aún no ha sido asignada.
    """
    return capacidades[mecanico][averia] == 1 and asignaciones[averia] == 0


def select(mecanico, capacidades, asignaciones, A):
    """
    Selecciona la mejor avería que un mecánico puede reparar, si es posible.

    :param mecanico: Índice del mecánico.
    :param capacidades: Matriz de capacidades de los mecánicos.
    :param asignaciones: Lista de asignaciones de averías.
    :param A: Número de averías.
    :return: Índice de la avería seleccionada o -1 si no hay ninguna disponible.
    """
    for averia in range(A):
        if factible(mecanico, averia, capacidades, asignaciones):
            return averia
    return -1


def solution(P, casos):
    """
    Resuelve el problema de asignación para cada caso de prueba.

    :param P: Número de casos de prueba.
    :param casos: Lista de casos de prueba.
    :return: Lista con las soluciones de cada caso.
    """
    resultados = []

    for caso in casos:
        M, A, capacidades = caso['M'], caso['A'], caso['capacidades']
        asignaciones = [0] * A  # Inicializa las asignaciones
        averias_reparadas = 0

        for mecanico in range(M):
            averia_seleccionada = select(mecanico, capacidades, asignaciones, A)
            if averia_seleccionada != -1:
                asignaciones[averia_seleccionada] = mecanico + 1  # Asigna el mecánico
                averias_reparadas += 1

        resultados.append((averias_reparadas, asignaciones))

    return resultados


if __name__ == '__main__':
    file_paths = encontrar_archivos_in(os.path.dirname(__file__))

    for file_path in file_paths:
        P, casos = leer_entrada(file_path)
        resultados = solution(P, casos)

        print(P)
        for resultado in resultados:
            print(resultado[0])
            print(f"{' '.join(map(str, resultado[1]))}")
        print()
