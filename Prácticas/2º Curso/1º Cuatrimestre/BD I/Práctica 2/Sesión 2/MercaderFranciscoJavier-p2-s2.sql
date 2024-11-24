-- Q1
select I.nombre nombre_instalacion, A.nombre nombre_actividad, M.nombre nombre_responsable
from instalacion I
JOIN actividad A ON I.instalacion_id = A.instalacion_id
JOIN monitor M ON A.responsable = M.dni
where A.precio < 10 and (I.M2 between 400 and 1500) and M.salario > 1000
order by nombre_actividad;

-- Q2
SELECT I.nombre nombre_instalacion,
       COALESCE(A.nombre, '*') nombre_actividad,
       COALESCE(M.nombre, '###') nombre_responsable
FROM INSTALACION I
LEFT JOIN ACTIVIDAD A ON I.instalacion_id = A.INSTALACION_ID
LEFT JOIN MONITOR M ON A.responsable = M.dni
ORDER BY I.nombre, A.nombre;

-- Q3
SELECT M.NOMBRE, M.telefono
FROM MONITOR M
WHERE M.dni IN (
    SELECT responsable
    FROM ACTIVIDAD
    WHERE nivel = 4
    )

UNION

SELECT M.nombre, M.telefono
FROM MONITOR M
WHERE M.dni IN (
    SELECT S.monitor_id
    FROM SESION S
    JOIN ACTIVIDAD A ON S.actividad_id = A.actividad_id
    WHERE A.nivel = 5
    )
ORDER BY telefono;