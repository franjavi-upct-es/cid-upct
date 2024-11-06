import numpy as np

def validador_E_AR(fichero_entrada, fichero_salida, fichero_salida_profesor=None):
    
    """
    Función que valida el algoritmo implementado para el ejercicio E_AR.
    Parámetros:
        * fichero_entrada: ruta al fichero con los datos de entrada con los que se ha alimentado el algoritmo propuesto.
        * fichero_salida: ruta al fichero con los resultados generados por el algoritmo propuesto.
        * fichero_salida_profesor: ruta al fichero con los resultados de prueba proporcionados por el profesor (opcional).
    """
    
    file_salida= open(fichero_salida)
    num_pruebas_salida= int(file_salida.readline())

    
    file_salida_prof= None
    if fichero_salida_profesor is not None:
        file_salida_prof= open(fichero_salida_profesor)
        file_salida_prof.readline()
    
    contador = 0
    porcentaje_acumulado = 0

    with open(fichero_entrada) as file:
        num_pruebas= int(file.readline())
        
        for i in range(num_pruebas):

            M,A = [int(number) for number in file.readline().strip().split(' ')]  

            mat_= []
            for j in range(0,M):
                a = [int(number) for number in file.readline().strip().split(' ')]  
                mat_.append(a)

            capacidad_mecanicos= np.vstack(mat_)  
            
            averias_reparadas= int(file_salida.readline())
            s= [int(number) for number in file_salida.readline().strip().split(' ')]
            
            averias_reparadas_prof= None
            if file_salida_prof:
                averias_reparadas_prof= int(file_salida_prof.readline())
                s_prof= [int(number) for number in file_salida_prof.readline().strip().split(' ')] 
            
            s_np= np.array(s)
            if len(s_np[s_np!=0]) != len(set(s_np[s_np!=0])):
                print(f"ERROR en el caso {i}: a un mecánico se le ha asignado más de una avería.")
            else:
                averias_reparadas_calculado= len(np.where(np.array(s)!=0)[0])
                if averias_reparadas != averias_reparadas_calculado:
                    print(f"ERROR en el caso {i}: número de averias no se ha calculado correctamente. Averías indicadas: {averias_reparadas}. Averías correctas: {averias_reparadas_calculado}")
                elif (averias_reparadas_prof is not None):
                    # and (ratio_variacion is not None) and (averias_reparadas < (averias_reparadas_prof * (1-ratio_variacion)))
                    if averias_reparadas > averias_reparadas_prof:
                        print (f"En el caso {i}: El porcentaje de averías reparadas de tu algoritmo {averias_reparadas}, es superior al de los profesores {averias_reparadas_prof}.")
                    elif averias_reparadas == averias_reparadas_prof:
                        contador += 1
                        porcentaje_acumulado += 100
                        print (f"En el caso {i}: Todo correcto y el porcentaje de averías reparadas es del 100%.")
                    else:
                        porcentaje = 100-(((averias_reparadas_prof-averias_reparadas) / averias_reparadas) * 100)
                        contador += 1
                        porcentaje_acumulado += porcentaje
                        print (f"En el caso {i}: Todo correcto y el porcentaje de averías reparadas ({averias_reparadas},{averias_reparadas_prof}) es del {round(porcentaje,2)}%.")
                else:
                    print(f"Todo correcto para el caso {i}.")

    print(f"La media porcentual para {contador} casos es del {round(porcentaje_acumulado/contador,2)}%.")