SELECT nombre, nivel, precio, cuantas_sesiones
FROM ACTIVIDAD A
    JOIN (SELECT actividad_id, COUNT(*) cuantas_sesiones
          FROM SESION
          GROUP BY actividad_id
          HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                             FROM SESION
                             GROUP BY actividad_id)) S ON S.actividad_id = A.actividad_id
ORDER BY nombre;

SELECT nombre, fcontrato
FROM MONITOR M
WHERE NOT EXISTS(
    SELECT actividad_id
    FROM ACTIVIDAD A
    WHERE NOT EXISTS(
        SELECT monitor_id
        FROM ESPECIALISTA E
        WHERE A.actividad_id = E.actividad_id AND M.dni = monitor_id
    )
);

SELECT I.nombre, COALESCE(ROUND(AVG(A.precio), 2), -1) media_precio
FROM INSTALACION I
    LEFT JOIN ACTIVIDAD A ON I.instalacion_id = A.instalacion_id
GROUP BY I.nombre
ORDER BY I.nombre DESC;

SELECT I.nombre,
       COALESCE(ROUND(AVG(A.precio), 2), -1) media_precio,
       COALESCE(A2.cuantas_actividades, 0) cuantas_actividades
FROM INSTALACION I
    LEFT JOIN ACTIVIDAD A ON I.instalacion_id = A.instalacion_id
    LEFT JOIN (SELECT instalacion_id, COUNT(*) cuantas_actividades
               FROM ACTIVIDAD A
                JOIN SESION S ON A.actividad_id = S.actividad_id
                    AND A.responsable = S.monitor_id
               GROUP BY instalacion_id) A2 ON I.instalacion_id = A2.instalacion_id
GROUP BY I.nombre, A2.cuantas_actividades
ORDER BY I.nombre DESC;
