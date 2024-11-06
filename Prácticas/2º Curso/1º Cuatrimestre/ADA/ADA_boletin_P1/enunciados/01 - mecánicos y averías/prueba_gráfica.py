import time
import matplotlib.pyplot as plt
from mecánicos_y_averias import encontrar_archivos_in, leer_entrada, solution

def analyze_complexity(file_paths):
    """
    Mide el tiempo de ejecución para cada archivo y genera un gráfico comparativo.

    :param file_paths: Lista de rutas de archivos `.in`.
    """
    sizes = []
    times = []

    for file_path in file_paths:
        # Medir el tiempo de ejecución para leer y procesar cada archivo
        start_time = time.time()

        # Leer la entrada y procesar los casos de prueba
        P, casos = leer_entrada(file_path)
        resultados = solution(P, casos)

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Calcular el tamaño aproximado de la entrada
        with open(file_path, 'r') as f:
            size = sum(1 for _ in f)

        # Agregar el tamaño y tiempo a las listas
        sizes.append(size)
        times.append(elapsed_time)

    # Graficar el resultado comparativo para todos los archivos
    plt.plot(sizes, times, marker='o', linestyle='--')
    plt.xlabel('Tamaño aproximado')
    plt.ylabel('Tiempo (s)')
    plt.show()


# Ejecuta el análisis de complejidad en todos los archivos `.in` en el directorio actual
if __name__ == '__main__':
    file_paths = encontrar_archivos_in('.')
    analyze_complexity(file_paths)
