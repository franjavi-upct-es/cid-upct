import os

def encontrar_archivos_in(directorio='.'):
    archivos_in = []
    for root, _, files in os.walk(directorio):
        for file in files:
            if file.endswith('.in'):
                archivos_in.append(os.path.join(root, file))
    return archivos_in

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

# Función de backtracking basada en el esquema "backtracking_todas"
def backtracking_todas(s_inicial, M, A, capacidades):
    nivel = 1
    s = s_inicial
    fin = False
    soluciones = []

    while nivel != 0:
        s = generar(nivel, s, M, A)

        if solucion(nivel, s, A):
            almacenar(soluciones, s, A)

        if criterio(nivel, s, capacidades, A):
            nivel += 1
        else:
            while not masHermanos(nivel, s, A) and nivel > 0:
                s = retroceder(nivel, s)
                nivel -= 1

    return soluciones

# Genera el siguiente candidato en el nivel actual
def generar(nivel, s, M, A):
    if s[nivel - 1] < M:  # Si el valor en el nivel es menor que el número de mecánicos
        s[nivel - 1] += 1
    return s

# Verifica si se ha encontrado una solución completa (todas las averías tienen un mecánico asignado)
def solucion(nivel, s, A):
    return nivel == A + 1  # Se alcanza una solución cuando se han asignado todas las averías

# Almacena la solución en la lista de soluciones válidas
def almacenar(soluciones, s, A):
    soluciones.append(s[:A])  # Añadir una copia de la solución parcial hasta el nivel actual

# Criterio para continuar explorando soluciones: verificar si el mecánico puede asignarse a la avería actual
def criterio(nivel, s, capacidades, A):
    mecanico = s[nivel - 1] - 1
    averia = nivel - 1
    return (0 <= mecanico < len(capacidades) and
            0 <= averia < len(capacidades[mecanico]) and
            capacidades[mecanico][averia] == 1)

# Verifica si existen más opciones en el nivel actual
def masHermanos(nivel, s, A):
    return s[nivel - 1] < A

# Retrocede un nivel y deshace la última asignación
def retroceder(nivel, s):
    s[nivel - 1] = 0
    return s

# Procesar cada caso de prueba
def solution(P, casos):
    resultados = []
    for caso in casos:
        M, A, capacidades = caso['M'], caso['A'], caso['capacidades']
        s_inicial = [0] * (A + 1)  # Solución inicial: sin asignaciones
        soluciones = backtracking_todas(s_inicial, M, A, capacidades)

        # Contar averías reparadas en la mejor solución y el detalle de asignaciones
        averias_reparadas = max(len([x for x in sol if x > 0]) for sol in soluciones)
        mejor_solucion = max(soluciones, key=lambda sol: len([x for x in sol if x > 0]))

        resultados.append((averias_reparadas, mejor_solucion))

    return resultados

file_paths = encontrar_archivos_in(os.path.dirname(__file__))

for file_path in file_paths:
    P, casos = leer_entrada(file_path)
    resultados = solution(P, casos)

if __name__ == '__main__':
    print(P)
    for resultado in resultados:
        print(resultado[0])
        print(f"{' '.join(map(str, resultado[1]))}"),