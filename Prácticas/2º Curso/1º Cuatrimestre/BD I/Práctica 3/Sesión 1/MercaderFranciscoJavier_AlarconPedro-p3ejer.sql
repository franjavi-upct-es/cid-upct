/*
Asignatura: Bases de Datos I
Curso académico: 2024/25
Convocatoria: Enero
P3. Definición y modificación de datos en SQL
Autores:
- Francisco Javier Mercader Martínez
- Pedro Alarcón Fuentes
*/

-- 2
-- a) Obtener el listado de freelances que colaboran con más de 2 revistas

SELECT F.dni, F.nombre, C.revista, C.pago_articulo
FROM FREELANCE F
    JOIN COLABORACION C ON C.freelance = F.dni
WHERE F.dni IN (SELECT freelance
                FROM COLABORACION
                GROUP BY freelance
                HAVING COUNT(revista) > 2)
ORDER BY F.dni, C.revista;

-- b) Aumentar un 3% los pagos por artículo y comprobar los cambios
UPDATE COLABORACION
SET pago_articulo = pago_articulo * 1.03
WHERE freelance IN (SELECT freelance
                    FROM COLABORACION
                    GROUP BY freelance
                    HAVING COUNT(revista) > 2);

SELECT F.dni, F.nombre, C.revista, C.pago_articulo
FROM FREELANCE F
    JOIN COLABORACION C ON C.freelance = F.dni
WHERE F.dni IN (SELECT freelance
                FROM COLABORACION
                GROUP BY freelance
                HAVING COUNT(revista) > 2)
ORDER BY F.dni, C.revista;

-- C) Deshacer la modificación utilizando ROLLBACK
ROLLBACK;

SELECT F.dni, F.nombre, C.revista, C.pago_articulo
FROM FREELANCE F
    JOIN COLABORACION C ON C.freelance = F.dni
WHERE F.dni IN (SELECT freelance
                FROM COLABORACION
                GROUP BY freelance
                HAVING COUNT(revista) > 2)
ORDER BY F.dni, C.revista;

-- 3
-- a) Cambiar el DNI de '11223344P' a '99001122P'
ALTER TABLE REVISTA DISABLE CONSTRAINT coordinador_fk_contratado;
ALTER TABLE ARTICULO DISABLE CONSTRAINT articulo_fk_contratado;
ALTER TABLE CONTRATADO DISABLE CONSTRAINT contratado_fk_tutor;

UPDATE REVISTA SET coordinador = '99001122P'
WHERE coordinador = '11223344P';

UPDATE ARTICULO SET contratado = '99001122P'
WHERE contratado = '11223344P';

UPDATE CONTRATADO SET tutor = '99001122P'
WHERE tutor = '11223344P';

UPDATE CONTRATADO SET dni = '99001122P'
WHERE dni = '11223344P';

ALTER TABLE REVISTA ENABLE CONSTRAINT coordinador_fk_contratado;
ALTER TABLE ARTICULO ENABLE CONSTRAINT articulo_fk_contratado;
ALTER TABLE CONTRATADO ENABLE CONSTRAINT contratado_fk_tutor;

SELECT * FROM CONTRATADO WHERE dni = '99001122P';
SELECT * FROM REVISTA WHERE coordinador = '99001122P';
SELECT * FROM ARTICULO WHERE contratado = '99001122P';
SELECT * FROM CONTRATADO WHERE tutor = '99001122P';

-- Confirmar los cambios
COMMIT;