import os
from E_AR_validador import validador_E_AR

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

def voraz(c, num_averias, mecanicos):
    s = []
    while len(c) > 0 and not solution(s, num_averias):
        x = select(c, mecanicos)
        c.remove(x)
        if factible(s, x):
            s.append(x)
    return s

def solution(P, casos):
    resultados = []

    for caso in casos:
        M, A, capacidades = caso['M'], caso['A'], caso['capacidades']

        asignaciones = [0] * A
        averias_reparadas = 0

        for mecanico in range(M):
            averia_seleccionada = select(mecanico, capacidades, asignaciones, A)
            if averia_seleccionada != -1:
                asignaciones[averia_seleccionada] = mecanico + 1
                averias_reparadas += 1

        resultados.append((averias_reparadas, asignaciones))

    return resultados

def select(mecanico, capacidades, asignaciones, A):
    for averia in range(A):
        if factible(mecanico, averia, capacidades, asignaciones):
            return averia
    return -1

def factible(mecanico, averia, capacidades, asignaciones):
    return capacidades[mecanico][averia] == 1 and asignaciones[averia] == 0

def procesar_matriz(matriz):
    num_averias = matriz.shape[1]
    candidatos = [(i, j) for i in range(matriz.shape[0]) for j in range(matriz.shape[1]) if matriz[i][j] == 1]
    solucion = voraz(candidatos, num_averias, matriz)
    resultado = [0] * num_averias
    for i, j in solucion:
        resultado[j] = i + 1
    return resultado

def generar_salida(matrices):
    casos = []
    for matriz in matrices:
        M = len(matriz)
        A = len(matriz[0]) if M > 0 else 0
        capacidades = matriz

        casos.append({'M': M, 'A': A, 'capacidades': capacidades})
    resultados = solution([], casos)
    return resultados

file_paths_in = encontrar_archivos_in(directorio=directorio)
file_paths_out = encontrar_archivos_out(directorio=directorio)

if __name__ == '__main__':
    P, casos = leer_entrada(file_paths_in[0])
    matrices = [caso['capacidades'] for caso in casos]
    resultados = generar_salida(matrices)
    print(P)
    for resultado in resultados:
        print(resultado[0])
        print(f"{' '.join(map(str, resultado[1]))}")

    for file_path in file_paths_in:
        output_name = os.path.splitext(file_path)[0] + '_out.txt'
        output_file = os.path.join(directorio, output_name)

        P, casos = leer_entrada(file_path)

        matrices = [caso['capacidades'] for caso in casos]
        resultados = generar_salida(matrices)

        with open(output_file, 'w') as file:
            file.write(f"{P}\n")
            for resultado in resultados:
                file.write(f"{resultado[0]}\n")
                file.write(" ".join(map(str, resultado[1])) + "\n")

        corresponding_out_file = os.path.splitext(file_path)[0] + '.out'
        if os.path.exists(corresponding_out_file):
            print(f"\nValidando {corresponding_out_file}...")
            validador_E_AR(fichero_entrada=file_path, fichero_salida=output_file, fichero_salida_profesor=corresponding_out_file)
            # Se eliminan las salidas del algoritmo para evitar archivos residuales
            os.remove(output_file)
        else:
            print(f"Archivo de salida del profesor no encontrado para {file_path}")

