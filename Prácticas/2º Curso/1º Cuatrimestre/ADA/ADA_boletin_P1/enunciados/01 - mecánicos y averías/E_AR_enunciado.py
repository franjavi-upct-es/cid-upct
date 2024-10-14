import os
import pandas as pd


def procesar_fichero(ruta_fichero):
    # Contruir la ruta completa del fichero
    directory = os.path.join(os.path.dirname(__file__), "tests", "T1")
    fichero_path = os.path.join(directory, ruta_fichero)

    # Leer el fichero
    with open(fichero_path, 'r') as fichero:
        # Leer la primera línea
        num_tablas = int(fichero.readline().strip())

        # Leer las siguientes líneas
        dimensiones = []

        # Leer las siguientes líneas
        for linea in fichero:
            valores = [int(x) for x in linea.strip().split()]
            if any(x not in [0, 1] for x in valores):
                dimensiones.append(valores)

        # Crear un DataFrame con las diferentes dimensiones
        df = pd.DataFrame(dimensiones, columns=['Filas', 'Columnas'])

        return df
    
if __name__ == "__main__":
    ruta_fichero = '701a.in'
    df_resultado = procesar_fichero(ruta_fichero)
    print(df_resultado)
