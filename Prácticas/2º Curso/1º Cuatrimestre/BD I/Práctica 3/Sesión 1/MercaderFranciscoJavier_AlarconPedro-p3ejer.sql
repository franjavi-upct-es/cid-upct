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

-- 4
-- a)                   
SELECT A.titulo, N.fecha
FROM articulo A
JOIN NUMERO N ON A.revista = N.revista
WHERE N.fecha < TO_DATE('31/12/2023', 'DD/MM/YYYY')
AND A.contratado NOT IN (SELECT coordinador
                      FROM revista);
                      
DELETE FROM ARTICULO 
WHERE titulo IN (SELECT A.titulo
                FROM articulo A
                JOIN NUMERO N ON A.revista = N.revista
                WHERE N.fecha < TO_DATE('31/12/2023', 'DD/MM/YYYY')
                AND A.contratado NOT IN (SELECT coordinador
                                        FROM revista));
-- b)                                        
COMMIT;

-- 5
ALTER TABLE REVISTA DISABLE CONSTRAINT coordinador_fk_contratado;

DELETE FROM ARTICULO 
WHERE revista = 'R01';

DELETE FROM NUMERO 
WHERE revista = 'R01';

DELETE FROM CONTRATADO
WHERE revista = 'R01';

DELETE FROM COLABORACION 
WHERE revista = 'R01';

DELETE FROM REVISTA 
WHERE idrev = 'R01';

ALTER TABLE REVISTA ENABLE CONSTRAINT coordinador_fk_contratado;

COMMIT;

-- 6
-- a)
ALTER TABLE REVISTA DROP COLUMN web;
ALTER TABLE REVISTA DROP COLUMN periodicidad;

SELECT * FROM REVISTA;

-- b)

/* 
Si es posible, la sentencia sería ALTER TABLE REVISTA DROP COLUMN (web, periodicidad);
*/

-- 7
-- a)
CREATE OR REPLACE VIEW CONTRATO
AS SELECT
        R.nombre revista,
        C.nombre periodista,
        C.sueldo sueldo,
        C.fecha_contrato contrato,
        2024 - EXTRACT(YEAR FROM C.fecha_contrato) annos,
        NVL((SELECT COUNT(*)
            FROM ARTICULO A
            WHERE A.contratado = C.dni AND A.revista = R.idrev), 0) AS articulos
FROM revista R
        LEFT JOIN CONTRATADO C ON C.revista = R.idrev;

-- b)
SELECT * FROM CONTRATO
ORDER BY revista, periodista;

-- c)
CREATE OR REPLACE VIEW CONTRATO AS 
SELECT
    R.nombre revista,
    C.nombre periodista,
    C.sueldo * 0.79 sueldo,
    C.fecha_contrato contrato,
    2024 - EXTRACT(YEAR FROM C.fecha_contrato) annos,
    NVL((SELECT COUNT(*)
        FROM ARTICULO A
        WHERE A.contratado = C.dni AND A.revista = R.idrev), 0) AS articulos
FROM revista R
LEFT JOIN CONTRATADO C ON C.revista = R.idrev;

-- d)
INSERT INTO CONTRATADO (dni, nombre, email, sueldo, revista, fecha_contrato, tutor)
VALUES ('99002211X', 'NUEVO PERIODISTA', 'nperiodista@mail.com', 2300, 'R03', TO_DATE('20/05/2018', 'DD/MM/YYYY'), NULL);

-- e)
SELECT * FROM CONTRATO
ORDER BY revista, periodista;

-- f)
COMMIT;

-- 8
-- a)
/*
CREATE ASSERTION CoordinadorEsContratado
CHECK (
       NOT EXISTS (
            SELECT 1
            FROM REVISTA R
            WHERE R.coordinador NOT IN (
                SELECT C.dni
                FROM CONTRATADO C
                WHERE R.revista = R.idrev
            )
    )
);
*/

-- 9
SELECT C.nombre periodista, R.nombre revista, C.sueldo
FROM CONTRATADO C
    JOIN REVISTA R ON C.revista = R.idrev
WHERE C.sueldo = (SELECT MAX(sueldo)
                  FROM CONTRATADO CC
                  WHERE CC.revista = C.revista);
-- a) COST inicial = 11
-- b)
CREATE INDEX idx_contratado_revista_sueldo
ON CONTRATADO (revista, sueldo);

-- c) COST = 8
/*
El índice ha mejorado el rendimiento de la consulta
*/