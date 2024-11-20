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

-- 5
SELECT nombre, telefono, TO_CHAR(fcontrato, 'Month') mes_contratado
FROM MONITOR
WHERE nombre LIKE '%cia%';

-- 6
SELECT actividad_id, diasemana ||' '|| hora dia_hora, monitor_id FROM SESION
WHERE (diasemana = 'M' OR diasemana = 'J')
  AND hora < 19
ORDER BY dia_hora;

-- 7
SELECT A.actividad_id, A.precio * 0.93 nuevo_precio
FROM ACTIVIDAD A
WHERE A.nivel = 5 and A.precio > 12;

-- 8
SELECT M.dni, M.nombre, M.salario, EXTRACT(YEAR FROM SYSDATE) - EXTRACT(YEAR FROM fcontrato) experiencia
FROM MONITOR M
WHERE EXTRACT(YEAR FROM SYSDATE) - EXTRACT(YEAR FROM fcontrato) >= 15;

-- 9
SELECT S.actividad_id, S.hora, S.monitor_id
FROM SESION S
WHERE S.actividad_id IN ('A02', 'A05', 'A09', 'A19')
    AND S.diasemana = 'V'
ORDER BY S.monitor_id;

-- 10
SELECT UNIQUE I.instalacion_id
FROM INSTALACION I
    JOIN ACTIVIDAD A ON I.instalacion_id = A.instalacion_id
WHERE A.nivel IN (1, 2)
ORDER BY I.instalacion_id ASC;

-- 11
SELECT A.nombre nombre_actividad, I.nombre nombre_instalacion, I.m2
FROM INSTALACION I
    JOIN ACTIVIDAD A ON A.instalacion_id = I.instalacion_id
WHERE A.nombre IN ('Pilates', 'Balonmano');

-- 12
SELECT DISTINCT A.actividad_id, S.hora, M.nombre nombre_monitor
FROM MONITOR M
    JOIN ACTIVIDAD A ON A.responsable = M.dni
    JOIN SESION S ON S.monitor_id = M.dni
WHERE A.actividad_id IN ('A02', 'A05', 'A09', 'A19') AND S.hora >= 15 AND S.diasemana = 'V'
ORDER BY S.hora;

-- 13
SELECT A.nombre, A.precio, A.nivel, I.nombre
FROM ACTIVIDAD A
    JOIN INSTALACION I ON I.instalacion_id = A.instalacion_id
WHERE I.tipo = 'Exterior';

-- 14
SELECT DISTINCT M.nombre nombre_monitor, A.nombre nombre_actividad
from SESION S
    JOIN ACTIVIDAD A ON S.actividad_id = A.actividad_id
    JOIN MONITOR M ON S.monitor_id = M.dni
WHERE hora >= 19 AND nivel IN (4, 5);

-- 15
SELECT I.tipo, A.nombre nombre_actividad, A.nivel, S.diasemana
FROM SESION S
    JOIN ACTIVIDAD A ON S.actividad_id = A.actividad_id
    JOIN INSTALACION I ON A.instalacion_id = I.instalacion_id
WHERE S.diasemana IN ('V', 'S')
ORDER BY S.diasemana DESC;

-- 16
SELECT M.nombre nombre_monitor, A.nombre nombre_actividad
FROM MONITOR M
    JOIN ACTIVIDAD A ON A.responsable = M.dni
    JOIN ESPECIALISTA E ON E.monitor_id = M.dni
ORDER BY M.nombre;

-- 17
SELECT I.nombre nombre_instalacion, I.tipo, M.nombre nombre_monitor
FROM INSTALACION I
    JOIN ACTIVIDAD A ON A.instalacion_id = I.instalacion_id
    JOIN MONITOR M ON A.responsable = M.dni
WHERE A.nombre IN ('Yoga', 'Body combat', 'Hapkido');

-- 18
SELECT S.diasemana, S.hora, A.nombre nombre_actividad, M.nombre nombre_monitor
FROM SESION S
    JOIN ACTIVIDAD A ON S.actividad_id = A.actividad_id
    JOIN MONITOR M ON A.responsable = M.dni
WHERE S.diasemana IN ('L', 'X');

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

-- 21
SELECT I.nombre nombre_instalacion, COALESCE(A.nombre, '----') nombre_actividad
FROM INSTALACION I
    LEFT JOIN ACTIVIDAD A ON A.instalacion_id = I.instalacion_id
ORDER BY I.nombre;

-- 22
SELECT monitor_id
FROM SESION
MINUS
SELECT responsable
FROM ACTIVIDAD;

-- 23
SELECT responsable
FROM ACTIVIDAD
WHERE nivel = 5

UNION

SELECT E.monitor_id responsable
FROM ESPECIALISTA E
    JOIN ACTIVIDAD A ON A.actividad_id = E.actividad_id
WHERE A.nivel = 2;

-- 24
SELECT A.actividad_id
FROM ACTIVIDAD A
    JOIN INSTALACION I ON A.instalacion_id = I.instalacion_id
WHERE I.tipo = 'Exterior'

INTERSECT

SELECT actividad_id
FROM SESION
WHERE diasemana = 'V';

-- 25
SELECT dni
FROM MONITOR
WHERE EXTRACT(YEAR FROM SYSDATE) - EXTRACT(YEAR FROM fcontrato) > 12

INTERSECT

SELECT DISTINCT monitor_id
FROM SESION

INTERSECT

SELECT monitor_id
FROM SESION
WHERE hora >= 16;