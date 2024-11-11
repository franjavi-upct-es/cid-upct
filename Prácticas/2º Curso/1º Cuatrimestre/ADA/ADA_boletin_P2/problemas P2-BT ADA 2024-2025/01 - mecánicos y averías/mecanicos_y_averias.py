import os

directorio = os.path.dirname(__file__)

def encontrar_archivos_in(directorio='.'):
    archivos_in = []
    for root, _, files in os.walk(directorio):
        for file in files:
            if file.endswith('.in'):
                archivos_in.append(os.path.join(root, file))
    return archivos_in


def encontrar_archivos_out(directorio='.'):
    archivos_out = []
    for root, _, files in os.walk(directorio):
        for file in files:
            if file.endswith('.out'):
                archivos_out.append(os.path.join(root, file))
    return archivos_out


def leer_entrada(file_path):
    with open(file_path, 'r') as file:
        lineas = file.readlines()

    P = int(lineas[0])
    casos = []

    indice = 1
    for _ in range(P):
        M, A = map(int, lineas[indice].split())
        indice += 1

        capacidades = []
        for i in range(M):
            capacidades.append(list(map(int, lineas[indice].split())))
            indice += 1

        casos.append({'M': M, 'A': A, 'capacidades': capacidades})

    return P, casos


def factible(mecanico, averia, capacidades, asignaciones):
    return capacidades[mecanico][averia] == 1 and asignaciones[averia] == 0


def backtrack(mecanico, averias_reparadas, asignaciones, capacidades, M, A, soluciones):
    # Si todas las averías han sido asignadas, guardamos la solución
    if averias_reparadas == A:
        soluciones.append(list(asignaciones))  # Guarda una copia de la asignación actual
        return True

    if mecanico >= M:
        return False  # No hay más mecánicos para asignar

    # Intentamos asignar este mecánico a cada avería posible
    for averia in range(A):
        if factible(mecanico, averia, capacidades, asignaciones):
            # Asignamos la avería al mecánico
            asignaciones[averia] = mecanico + 1
            averias_reparadas += 1

            # Llamada recursiva al siguiente mecánico
            if backtrack(mecanico + 1, averias_reparadas, asignaciones, capacidades, M, A, soluciones):
                return True  # Se encontró una solución válida

            # Retroceso: Deshacemos la asignación
            asignaciones[averia] = 0
            averias_reparadas -= 1

    # Intentamos el siguiente mecánico sin asignaciones
    return backtrack(mecanico + 1, averias_reparadas, asignaciones, capacidades, M, A, soluciones)


def solution_backtracking(P, casos):
    resultados = []

    for caso in casos:
        M, A, capacidades = caso['M'], caso['A'], caso['capacidades']
        asignaciones = [0] * A  # Inicialmente, ninguna avería está asignada
        soluciones = []  # Almacena soluciones posibles

        # Llamada inicial al algoritmo de backtracking
        backtrack(0, 0, asignaciones, capacidades, M, A, soluciones)

        # Si se encontró una solución, guardamos la primera (u otra lógica si quieres múltiples)
        if soluciones:
            averias_reparadas = sum(1 for x in soluciones[0] if x != 0)
            resultados.append((averias_reparadas, soluciones[0]))
        else:
            resultados.append((0, asignaciones))  # En caso de no encontrar ninguna solución

    return resultados


def generar_salida(matrices):
    casos = []
    for matriz in matrices:
        M = len(matriz)
        A = len(matriz[0]) if M > 0 else 0
        capacidades = matriz

        casos.append({'M': M, 'A': A, 'capacidades': capacidades})
    resultados = solution_backtracking(len(casos), casos)
    return resultados


file_paths_in = encontrar_archivos_in(directorio=directorio)

if __name__ == '__main__':
    P, casos = leer_entrada(file_paths_in[0])
    matrices = [caso['capacidades'] for caso in casos]
    resultados = generar_salida(matrices)
    print(P)
    for resultado in resultados:
        print(resultado[0])
        print(f"{' '.join(map(str, resultado[1]))}")