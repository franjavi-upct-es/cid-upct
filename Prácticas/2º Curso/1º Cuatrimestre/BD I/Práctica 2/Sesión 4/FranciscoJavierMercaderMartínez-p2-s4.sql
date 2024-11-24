-- 54
SELECT actividad_id
FROM ESPECIALISTA
GROUP BY actividad_id
HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                   FROM ESPECIALISTA
                   GROUP BY actividad_id);

-- 55
SELECT actividad_id, COUNT(*) cuantas_sesiones
FROM SESION
GROUP BY actividad_id
HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                   FROM SESION
                   GROUP BY actividad_id);

-- 56
SELECT dni, nombre, salario
FROM MONITOR
WHERE dni IN (SELECT monitor_id
              FROM SESION
              GROUP BY monitor_id
              HAVING COUNT(*) = (
                  SELECT MIN(COUNT(*))
                  FROM SESION
                  GROUP BY monitor_id
                  ));

-- 57
SELECT instalacion_id, nombre, m2
FROM INSTALACION
WHERE instalacion_id IN (SELECT instalacion_id
                         FROM ACTIVIDAD
                         GROUP BY instalacion_id
                         HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                                            FROM ACTIVIDAD
                                            GROUP BY instalacion_id))
ORDER BY instalacion_id;

-- 58
SELECT nombre, precio
FROM ACTIVIDAD
WHERE actividad_id IN (SELECT actividad_id
                       FROM SESION
                       GROUP BY actividad_id
                       HAVING COUNT(*) = (SELECT MIN(COUNT(*))
                                          FROM SESION
                                          GROUP BY actividad_id));

-- 59
SELECT nombre, nivel, precio
FROM ACTIVIDAD
WHERE responsable IN (SELECT dni
                      FROM MONITOR
                      WHERE fcontrato IN (SELECT MIN(fcontrato)
                                          FROM MONITOR))
    AND actividad_id IN (SELECT actividad_id
                         FROM SESION
                         GROUP BY actividad_id
                         HAVING COUNT(*) > 2)
ORDER BY nombre;

-- 60
SELECT monitor_id, COUNT(*) sesiones_exteriores
FROM SESION
WHERE actividad_id IN (SELECT actividad_id
                       FROM ACTIVIDAD
                       WHERE instalacion_id IN (SELECT instalacion_id
                                                FROM INSTALACION
                                                WHERE tipo = 'Exterior'))
GROUP BY monitor_id
HAVING COUNT(*) = (SELECT ROUND(AVG(COUNT(*)))
                   FROM SESION
                   GROUP BY monitor_id);

-- 61
SELECT A.actividad_id, A.nombre nombre_actividad, M.nombre nombre_responsable
FROM ACTIVIDAD A
    JOIN MONITOR M ON A.responsable = M.dni
WHERE A.actividad_id IN (SELECT actividad_id
                         FROM ESPECIALISTA
                         GROUP BY actividad_id
                         HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                                            FROM ESPECIALISTA
                                            GROUP BY actividad_id));

-- 62
SELECT M.nombre nombre_monitor, A.nombre nombre_actividad, COUNT(*) sesiones_martes
FROM MONITOR M
    JOIN SESION S ON S.monitor_id = M.dni
    JOIN ACTIVIDAD A ON A.actividad_id = S.actividad_id
WHERE M.dni IN (SELECT dni
                FROM MONITOR
                WHERE salario IN (SELECT MIN(salario)
                                  FROM MONITOR))
    AND S.diasemana = 'M'
GROUP BY M.nombre, A.nombre
ORDER BY M.nombre, A.nombre;

-- 63
SELECT dni, nombre, cuantas_sesiones
FROM MONITOR
    JOIN (SELECT monitor_id, COUNT(*) cuantas_sesiones
          FROM SESION
          GROUP BY monitor_id) S ON dni = S.monitor_id
ORDER BY nombre;

-- 64
SELECT A.actividad_id, A.nombre, cuantas_sesiones
FROM ACTIVIDAD A
    JOIN (SELECT actividad_id, COUNT(*) cuantas_sesiones
          FROM SESION
          GROUP BY actividad_id) S ON S.actividad_id = A.actividad_id
ORDER BY A.actividad_id;

-- 65
SELECT DISTINCT M.nombre nombre_monitor, nombre_actividad
FROM MONITOR M
    JOIN (SELECT monitor_id, actividad_id
          FROM SESION
          WHERE diasemana = 'M' AND hora >= 16) S ON S.monitor_id = M.dni
    JOIN (SELECT actividad_id, nombre nombre_actividad
          FROM ACTIVIDAD
          WHERE nivel >= 4) A ON S.actividad_id = A.actividad_id
ORDER BY M.nombre;

-- 66
SELECT nombre, responsable, cuantas_sesiones
FROM ACTIVIDAD A
    JOIN (SELECT instalacion_id
          FROM INSTALACION
          WHERE tipo = 'Interior') I ON I.instalacion_id = A.instalacion_id
    JOIN (SELECT monitor_id, actividad_id, COUNT(*) cuantas_sesiones
          FROM SESION
          GROUP BY monitor_id, actividad_id) S ON S.monitor_id = A.responsable AND S.actividad_id = A.actividad_id;

-- 67
SELECT A.actividad_id, nombre, cuantos_especialistas
FROM ACTIVIDAD A
    JOIN (SELECT actividad_id, COUNT(*) cuantos_especialistas
          FROM ESPECIALISTA
          GROUP BY actividad_id
          HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                             FROM ESPECIALISTA
                             GROUP BY actividad_id)) E ON E.actividad_id = A.actividad_id;

-- 68
SELECT A.actividad_id, nombre, cuantas_sesiones
FROM ACTIVIDAD A
    JOIN (SELECT actividad_id, COUNT(*) cuantas_sesiones
          FROM SESION
          GROUP BY actividad_id
          HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                             FROM SESION
                             GROUP BY actividad_id)) S ON S.actividad_id = A.actividad_id;

-- 69
SELECT I.nombre, COALESCE(activ_2, 0) activ_2, COALESCE(activ_5, 0) activ_5
FROM INSTALACION I
    LEFT JOIN (SELECT instalacion_id, COUNT(*) activ_2
               FROM ACTIVIDAD
               WHERE nivel = 2
               GROUP BY instalacion_id) A ON A.instalacion_id = I.instalacion_id
    LEFT JOIN (SELECT instalacion_id, COUNT(*) activ_5
               FROM ACTIVIDAD
               WHERE nivel = 5
               GROUP BY instalacion_id) A2 ON A2.instalacion_id = I.instalacion_id
ORDER BY I.instalacion_id;

