/*
Asignatura: BASES DE DATOS I
Curso: 2024/25
Convocatoria: enero

Practica: P2. Consultas SQL

Usuario Oracle: bdixyy  <-- VUESTRO USUARIO AQUÍ
Estudiante(s): Francisco Javier Mercader Martínez <-- NOMBRES Y APELLIDOS

*/

-- CONSULTAS:

-- 1
SELECT nombre, telefono, salario FROM MONITOR
WHERE salario > 1200;

-- 2
SELECT nombre, responsable, nivel FROM ACTIVIDAD
WHERE nivel BETWEEN 1 AND 3;

-- 3
SELECT instalacion_id FROM ACTIVIDAD
WHERE nivel = 3 AND precio < 10
ORDER BY instalacion_id DESC;

-- 4
SELECT actividad_id, diasemana, hora FROM SESION
WHERE (diasemana = 'S' AND HORA BETWEEN 9 AND 11.3)
   OR diasemana = 'L'
ORDER BY diasemana, hora;

-- 6
SELECT actividad_id, diasemana ||' '|| hora dia_hora, monitor_id FROM SESION
WHERE (diasemana = 'M' OR diasemana = 'J')
  AND hora < 19
ORDER BY dia_hora;

-- 14
SELECT DISTINCT M.nombre nombre_monitor, A.nombre nombre_actividad
from SESION S
    JOIN ACTIVIDAD A ON S.actividad_id = A.actividad_id
    JOIN MONITOR M ON S.monitor_id = M.dni
WHERE hora >= 19 AND nivel IN (4, 5);

-- 19
SELECT diasemana, hora, A.nombre nombre_actividad, R.nombre nombre_responsable
FROM SESION S
    JOIN monitor M ON S.monitor_id = M.dni
    JOIN actividad A ON S.actividad_id = A.actividad_id
    JOIN monitor R ON A.responsable = R.dni
WHERE M.nombre = 'Belinda';

-- 20
SELECT COALESCE(A.nombre, '···') nombre_actividad, M.nombre nombre_responsable
FROM ACTIVIDAD A
    RIGHT JOIN monitor M ON A.responsable = M.dni
ORDER BY M.nombre;

-- 23
SELECT responsable FROM ACTIVIDAD
WHERE nivel = 5

UNION

SELECT E.monitor_id responsable FROM ESPECIALISTA E
    JOIN ACTIVIDAD A ON A.actividad_id = E.actividad_id
WHERE A.nivel = 2;