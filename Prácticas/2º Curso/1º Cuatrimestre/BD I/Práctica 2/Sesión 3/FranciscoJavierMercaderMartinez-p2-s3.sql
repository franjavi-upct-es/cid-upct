-- 22
SELECT dni
FROM MONITOR

MINUS

SELECT monitor_id
FROM SESION;

-- 23
SELECT responsable
FROM ACTIVIDAD
WHERE nivel = 5

UNION

SELECT monitor_id
FROM ESPECIALISTA E
    JOIN ACTIVIDAD A ON A.actividad_id = E.actividad_id
WHERE A.nivel = 2;

-- 24
SELECT actividad_id
FROM SESION
WHERE DIASEMANA = 'V'

INTERSECT

SELECT actividad_id
FROM ACTIVIDAD A
    JOIN INSTALACION I ON A.instalacion_id = I.instalacion_id
WHERE I.tipo = 'Exterior';

-- 25
SELECT dni
FROM MONITOR
WHERE 2024 - EXTRACT(YEAR FROM fcontrato) > 12

INTERSECT

SELECT DISTINCT monitor_id
FROM SESION
WHERE hora > 16;

-- 26
SELECT instalacion_id, nombre, tipo
FROM INSTALACION 
WHERE instalacion_id NOT IN (
    SELECT DISTINCT instalacion_id
    FROM ACTIVIDAD
);

-- 27
SELECT dni, nombre, LOWER(TO_CHAR(fcontrato, 'DD/MONTH/YYYY')) AS fcontrato
FROM MONITOR 
WHERE dni NOT IN (
    SELECT DISTINCT responsable
    FROM ACTIVIDAD)
ORDER BY EXTRACT(YEAR FROM TO_DATE(fcontrato));

-- 28
SELECT dni, nombre
FROM MONITOR
WHERE dni IN (
    SELECT responsable
    FROM ACTIVIDAD 
    WHERE nivel < 4 AND instalacion_id IN (
        SELECT instalacion_id
        FROM INSTALACION 
        WHERE m2 BETWEEN 50 AND 200
    )
);

-- 29
SELECT nombre
FROM MONITOR
WHERE dni IN (
  SELECT monitor_id
  FROM SESION
  WHERE diasemana = 'M' AND hora >= 16 AND actividad_id IN (
        SELECT actividad_id
        FROM ACTIVIDAD
        WHERE nivel >= 4
    )
);

-- 30
SELECT nombre, tipo
FROM INSTALACION
WHERE instalacion_id IN (
    SELECT instalacion_id
    FROM ACTIVIDAD
    WHERE nivel <= 2)
    AND instalacion_id NOT IN (
    SELECT instalacion_id
    FROM ACTIVIDAD
    WHERE nivel >= 3
);

-- 31
SELECT DISTINCT M.nombre, M.fcontrato
FROM MONITOR M
    JOIN SESION S ON S.monitor_id = M.dni
WHERE S.actividad_id NOT IN (
    SELECT E.actividad_id
    FROM ESPECIALISTA E
    WHERE E.monitor_id = S.monitor_id
);

-- 32
SELECT nombre
FROM MONITOR
WHERE dni IN (
    SELECT A.responsable
    FROM ACTIVIDAD A
    WHERE A.responsable NOT IN (
        SELECT S.monitor_id
        FROM SESION S
        WHERE S.actividad_id = A.actividad_id
    )
);


-- 33
SELECT M.nombre nombre_monitor, A.nombre nombre_actividad
FROM MONITOR M
    JOIN ACTIVIDAD A ON A.responsable = M.dni
WHERE A.instalacion_id IN (
    SELECT I.instalacion_id
    FROM INSTALACION I
    WHERE I.instalacion_id = A.instalacion_id AND I.m2 > 500
)
ORDER BY M.nombre;

-- 34
SELECT nombre
FROM INSTALACION
WHERE instalacion_id IN (
    SELECT instalacion_id
    FROM ACTIVIDAD
    WHERE nivel = 3 AND responsable IN (
        SELECT dni
        FROM MONITOR
        WHERE EXTRACT(YEAR FROM fcontrato) < 2018)
        AND actividad_id IN (
            SELECT actividad_id
            FROM SESION
            WHERE diasemana = 'S'
        )
);

-- 35
SELECT ROUND(AVG(numero_medio_sesiones)) numero_medio_sesiones
FROM (SELECT COUNT(monitor_id) numero_medio_sesiones
      FROM SESION
      GROUP BY monitor_id);

-- 36
SELECT nombre, fcontrato, salario
FROM MONITOR
WHERE salario = (SELECT MIN(SALARIO)
                 FROM MONITOR);

-- 37
SELECT actividad_id, COUNT(monitor_id) cuantos_monitores
FROM ESPECIALISTA
GROUP BY actividad_id
ORDER BY actividad_id;

-- 38
SELECT diasemana, COUNT(actividad_id) cuantas_sesiones
FROM SESION
GROUP BY diasemana
ORDER BY cuantas_sesiones DESC;

-- 39
SELECT hora, COUNT(actividad_id) cuantas_sesiones
FROM SESION
WHERE hora <= 13.3
GROUP BY hora
ORDER BY hora;

-- 40
SELECT monitor_id, diasemana, COUNT(monitor_id) cuantas_sesiones
FROM SESION
GROUP BY monitor_id, diasemana
ORDER BY monitor_id;

-- 41
SELECT instalacion_id, COUNT(actividad_id) cuantas_actividades
FROM ACTIVIDAD
GROUP BY instalacion_id
ORDER BY instalacion_id;

-- 42
SELECT monitor_id, COUNT(actividad_id) cuantas_sesiones
FROM SESION
WHERE monitor_id IN (SELECT dni
                    FROM MONITOR
                    WHERE salario BETWEEN 950 AND 1500)
GROUP BY monitor_id;

-- 43
SELECT M.dni, M.nombre, COUNT(S.actividad_id) cuantas_sesiones
FROM MONITOR M
    JOIN SESION S ON S.monitor_id = M.dni
GROUP BY M.dni, M.nombre
ORDER BY M.nombre;

-- 44
SELECT A.actividad_id, A.nombre, COUNT(S.actividad_id) cuantas_sesiones
FROM ACTIVIDAD A
    JOIN SESION S ON S.actividad_id = A.actividad_id
GROUP BY A.actividad_id, A.nombre
ORDER BY A.actividad_id;

-- 45
SELECT instalacion_id
FROM INSTALACION
WHERE instalacion_id IN (
    SELECT instalacion_id
    FROM ACTIVIDAD
    GROUP BY instalacion_id
    HAVING COUNT(instalacion_id) = 1
);

-- Ampliación
SELECT nombre, tipo, m2
FROM INSTALACION
WHERE instalacion_id IN (
    SELECT instalacion_id
    FROM ACTIVIDAD
    GROUP BY instalacion_id
    HAVING COUNT(instalacion_id) = 1
);

-- 46
SELECT nombre, nivel, precio
FROM ACTIVIDAD
WHERE RESPONSABLE IN (
    SELECT dni
    FROM MONITOR
    WHERE nombre = 'Auspicia'
) AND actividad_id IN (
    SELECT actividad_id
    FROM SESION
    GROUP BY actividad_id
    HAVING COUNT(actividad_id) > 2
    )
ORDER BY nombre;

-- 47
SELECT nombre, TO_CHAR(fcontrato, 'DD/MM/YY') fcontrato
FROM MONITOR
WHERE dni IN (
    SELECT monitor_id
    FROM SESION
    GROUP BY monitor_id
    HAVING COUNT(monitor_id) > 6
)
ORDER BY nombre;

-- 48
SELECT diasemana
FROM SESION
WHERE actividad_id IN (
    SELECT actividad_id
    FROM ACTIVIDAD
    WHERE instalacion_id IN (
        SELECT instalacion_id
        FROM INSTALACION
        WHERE tipo = 'Exterior'
    )
)
GROUP BY diasemana
HAVING COUNT(diasemana) > 3;

-- 49
SELECT M.dni, M.nombre, COUNT(S.monitor_id) cuantas_sesiones
FROM MONITOR M
    LEFT JOIN SESION S ON S.monitor_id = M.dni
GROUP BY M.dni, M.nombre
ORDER BY M.dni;

-- 50
SELECT M.dni, M.nombre, COUNT(E.actividad_id) cuantas_actividades
FROM MONITOR M
    LEFT JOIN ESPECIALISTA E ON E.monitor_id = M.dni
GROUP BY M.dni, M.nombre
ORDER BY cuantas_actividades;

-- 51
SELECT I.instalacion_id, COUNT(A.actividad_id) cuantas_actividades
FROM INSTALACION I
    LEFT JOIN ACTIVIDAD A ON A.instalacion_id = I.instalacion_id
GROUP BY I.instalacion_id
ORDER BY I.instalacion_id;

-- 52
SELECT A.responsable, A.actividad_id, COUNT(A.responsable) cuantas_sesiones
FROM ACTIVIDAD A
    JOIN SESION S ON S.actividad_id = A.actividad_id
WHERE S.monitor_id = A.responsable
GROUP BY A.responsable, A.actividad_id
ORDER BY A.actividad_id;

-- 53
SELECT A.nombre, A.responsable, COUNT(S.monitor_id) cuantas_sesiones
FROM ACTIVIDAD A
    JOIN SESION S ON S.actividad_id = A.actividad_id
WHERE instalacion_id IN (
    SELECT instalacion_id
    FROM INSTALACION
    WHERE tipo = 'Interior'
    ) AND A.responsable = S.monitor_id
GROUP BY A.nombre, A.responsable;