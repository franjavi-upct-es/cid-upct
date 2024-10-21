import os

def resolver_problema_asignacion_mecanicos(casos_de_prueba):
    resultados = [ ]

    for caso in casos_de_prueba:
        mecanicos, averias, matriz = caso
        asignaciones = [ -1 ] * averias  # -1 indica que la avería no tiene asignación
        mecanicos_asignados = [ False ] * mecanicos  # Para saber si un mecánico ya está asignado

        # Intentamos asignar mecanicos a las averias
        total_averias_reparadas = 0
        for j in range(averias):
            for i in range(mecanicos):
                if matriz [ i ] [ j ] == 1 and not mecanicos_asignados [ i ]:
                    # Asignamos el mecánico i a la avería j
                    asignaciones [ j ] = i + 1  # +1 porque los mecanicos comienzan en 1
                    mecanicos_asignados [ i ] = True
                    total_averias_reparadas += 1
                    break

        # Almacenamos los resultados para este caso
        resultados.append((total_averias_reparadas, asignaciones))

    return resultados


def procesar_entrada_y_resolver(archivo_contenido):
    lineas = archivo_contenido.strip().splitlines()
    num_casos = int(lineas [ 0 ].strip())  # Número total de casos de prueba
    i = 1
    casos_de_prueba = [ ]

    while i < len(lineas):
        mecanicos, averias = map(int, lineas [ i ].strip().split())
        i += 1
        matriz = [ ]
        for _ in range(mecanicos):
            fila = list(map(int, lineas [ i ].strip().split()))
            matriz.append(fila)
            i += 1
        casos_de_prueba.append((mecanicos, averias, matriz))

    resultados = resolver_problema_asignacion_mecanicos(casos_de_prueba)
    salida = [str(num_casos)]
    for total_reparadas, asignaciones in resultados:
        salida.append(str(total_reparadas))
        asignaciones = [ str(a if a != -1 else 0) for a in asignaciones ]
        salida.append(' '.join(asignaciones))

    return '\n'.join(salida)


def procesar_fichero(ruta_fichero):
    with open(ruta_fichero, 'r') as fichero:
        archivo_contenido = fichero.read()
        resultado = procesar_entrada_y_resolver(archivo_contenido)
        print(f"Resultados para {ruta_fichero}:\n{resultado}\n")


def buscar_y_procesar_archivos():
    base_directory = os.path.join(os.path.dirname(__file__), "tests")

    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".in"):
                file_path = os.path.join(root, file)
                print(f"Procesando archivo: {file_path}")
                procesar_fichero(file_path)

if __name__ == "__main__":
    buscar_y_procesar_archivos()