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

-- 70
SELECT M.nombre, COALESCE(n_responsable, 0) n_responsable, COALESCE(n_especialista, 0) n_especialista, COALESCE(n_sesiones, 0) n_sesiones
FROM MONITOR M
    LEFT JOIN (SELECT responsable, COUNT(*) n_responsable
               FROM ACTIVIDAD
               GROUP BY responsable) A ON A.responsable = M.dni
    LEFT JOIN (SELECT monitor_id, COUNT(*) n_especialista
               FROM ESPECIALISTA
               GROUP BY monitor_id) E ON E.monitor_id = M.dni
    LEFT JOIN (SELECT monitor_id, COUNT(*) n_sesiones
               FROM SESION
               GROUP BY monitor_id) S ON S.monitor_id = M.dni
ORDER BY M.nombre;

-- 71
SELECT nombre, nivel
FROM ACTIVIDAD A
WHERE NOT EXISTS(SELECT *
                 FROM MONITOR
                 WHERE dni NOT IN (SELECT monitor_id
                                   FROM ESPECIALISTA E
                                   WHERE A.actividad_id = E.actividad_id));

-- 72
SELECT nombre, m2
FROM INSTALACION
WHERE INSTALACION_ID IN (SELECT DISTINCT instalacion_id
                         FROM ACTIVIDAD A
                         JOIN SESION S1 ON S1.actividad_id = A.actividad_id
                         JOIN SESION S2 ON S2.actividad_id = A.actividad_id
                         WHERE S1.hora < 13.3 AND S2.hora >= 15)
ORDER BY nombre ASC;

-- 73
SELECT M.nombre nombre_monitor, A.nombre nombre_actividad, sesiones
FROM MONITOR M
    JOIN (SELECT actividad_id, monitor_id, COUNT(*) sesiones
          FROM SESION
          GROUP BY actividad_id, monitor_id
          HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                             FROM SESION
                             GROUP BY actividad_id, monitor_id)) S ON S.monitor_id = M.dni
    JOIN ACTIVIDAD A ON A.actividad_id = S.actividad_id;

-- 74
SELECT nombre, cuantos_especialistas, cuantas_sesiones
FROM ACTIVIDAD A
    JOIN (SELECT actividad_id, COUNT(*) cuantos_especialistas
          FROM ESPECIALISTA
          GROUP BY actividad_id) E ON E.actividad_id = A.actividad_id
    JOIN (SELECT actividad_id, COUNT(*) cuantas_sesiones
          FROM SESION
          GROUP BY actividad_id
          HAVING COUNT(*) = (SELECT MIN(COUNT(*))
                             FROM SESION
                             GROUP BY actividad_id)) S ON A.actividad_id = S.actividad_id
ORDER BY nombre;

-- 75
SELECT I.nombre, COALESCE(cuantas_sesiones, 0) cuantas_sesiones
FROM INSTALACION I
    LEFT JOIN (SELECT instalacion_id, COUNT(*) cuantas_sesiones
               FROM ACTIVIDAD A
                   JOIN SESION S ON S.actividad_id = A.actividad_id
               GROUP BY instalacion_id) A ON A.instalacion_id = I.instalacion_id
ORDER BY I.nombre;

-- 76
SELECT I.nombre, COALESCE(cuantas_sesiones, 0) cuantas_sesiones, COALESCE(cuantas_actividades, 0) cuantas_actividades
FROM INSTALACION I
    LEFT JOIN (SELECT instalacion_id, COUNT(*) cuantas_sesiones
               FROM ACTIVIDAD A
                   JOIN SESION S ON S.actividad_id = A.actividad_id
               GROUP BY instalacion_id) A ON A.instalacion_id = I.instalacion_id
    LEFT JOIN (SELECT instalacion_id, COUNT(*) cuantas_actividades
               FROM ACTIVIDAD
                   JOIN MONITOR M ON M.dni = responsable
               WHERE EXTRACT(YEAR FROM M.fcontrato) >= 2015
               GROUP BY instalacion_id) A2 ON A2.instalacion_id = I.instalacion_id
ORDER BY I.nombre;

-- 77
SELECT M.nombre, actividades_especialista, actividades_impartidas
FROM MONITOR M
    JOIN (SELECT monitor_id, COUNT(*) actividades_especialista
          FROM ESPECIALISTA
          GROUP BY monitor_id) E ON E.monitor_id = M.dni
    JOIN (SELECT responsable, COUNT(*) actividades_impartidas
          FROM ACTIVIDAD
          GROUP BY responsable) A ON A.responsable = M.dni
WHERE actividades_especialista = 2 * actividades_impartidas
ORDER BY M.nombre;

-- 78
SELECT nombre, sesiones_LX, sesiones_MJ
FROM ACTIVIDAD A
    JOIN (SELECT actividad_id, COUNT(*) sesiones_LX
          FROM SESION
          WHERE diasemana IN ('L', 'X')
          GROUP BY actividad_id) S1 ON S1.actividad_id = A.actividad_id
    JOIN (SELECT actividad_id, COUNT(*) sesiones_MJ
          FROM SESION
          WHERE diasemana IN ('M', 'J')
          GROUP BY actividad_id) S2 ON S2.actividad_id = A.actividad_id
WHERE sesiones_LX > sesiones_MJ
ORDER BY nombre;

-- 79
SELECT nombre, monitores_especialistas, monitores_sesiones
FROM ACTIVIDAD A
    JOIN (SELECT actividad_id, COUNT(DISTINCT monitor_id) monitores_especialistas
          FROM ESPECIALISTA
          GROUP BY actividad_id) E ON A.actividad_id = E.actividad_id
    JOIN (SELECT actividad_id, COUNT(DISTINCT monitor_id) monitores_sesiones
          FROM SESION
          GROUP BY actividad_id) S ON A.actividad_id = S.actividad_id
WHERE monitores_especialistas = 4 * monitores_sesiones
ORDER BY nombre;

-- 80
SELECT nombre, cuantos_especialistas, responsable, activ_responsable
FROM ACTIVIDAD A
    JOIN (SELECT actividad_id
          FROM SESION
          GROUP BY actividad_id
          HAVING COUNT(DISTINCT monitor_id) > 1) AVM ON A.actividad_id = AVM.actividad_id -- Actividades con Varios Monitores (AVM
    JOIN (SELECT actividad_id, COUNT(DISTINCT monitor_id) cuantos_especialistas
          FROM ESPECIALISTA
          GROUP BY actividad_id) E ON E.actividad_id = A.actividad_id
    JOIN (SELECT monitor_id, COUNT(DISTINCT actividad_id) activ_responsable
          FROM SESION
          GROUP BY monitor_id) S ON S.monitor_id = A.responsable;