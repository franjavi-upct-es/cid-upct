El enunciado del archivo describe un problema de asignación de recursos, en el que se busca optimizar la asignación de mecánicos a averías en una empresa de reparación de maquinaria pesada. El objetico es maximizar el número de averías reparadas diariamente, respetando la restricción de que cada mecánico puede atender solo una avería por día.

## Puntos clave del problema
1. **Entrada:**
    
    - Se proporciona un número de casos de prueba
    - Para cada caso de prueba, hay una matriz dimensional que representa las capacidades de los mecánicos (filas) para reparar diferentes averías (columnas). Un valor de 1 en la posición $(i,j)$ indica que el mecánico $i$ puede reparar la avería $j$, mientras que 0 indica que no.

2. **Objetivo:**

    - Asignar mecánicos a las averías de tal forma que se maximice el número de averías reparadas.
    - La solución se considera válidad si al menos se cubre el 60% de la solución optima.

3. **Salida:**

    - El número total de averías reparadas.
    - Por cada avería, el mecánico asignado o un 0 si la avería no fue reparada.