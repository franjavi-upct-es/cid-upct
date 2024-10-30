DROP TABLE REVISTA CASCADE CONSTRAINTS;
DROP TABLE ARTICULO CASCADE CONSTRAINTS;
DROP TABLE CONTRATADO CASCADE CONSTRAINTS;
DROP TABLE COLABORACION CASCADE CONSTRAINTS;
DROP TABLE FREELANCE CASCADE CONSTRAINTS;
DROP TABLE ESPECIALIDAD_FREELANCE CASCADE CONSTRAINTS;
DROP TABLE NUMERO CASCADE CONSTRAINTS;

-- Crear la tabla REVISTA
CREATE TABLE REVISTA (
    idrev NUMBER PRIMARY KEY,
    nombre VARCHAR2(50) UNIQUE NOT NULL ,
    web VARCHAR2(50),
    tema VARCHAR2(50),
    periodicidad VARCHAR2(50) CHECK ( periodicidad IN ('Semanal', 'Quincenal', 'Mensual', 'Bimestral', 'Trimestral', 'Anual') ),
    coordinador NUMBER
);

-- Crear la tabla NUMERO
CREATE TABLE NUMERO(
    numero NUMBER,
    fecha DATE,
    num_articulos NUMBER CHECK ( num_articulos > 0 ),
    revista NUMBER,
    PRIMARY KEY (revista, numero),
    CHECK ( numero > 0 )
);

-- Crear la tabla ARTICULO
CREATE TABLE ARTICULO (
    idart NUMBER PRIMARY KEY,
    titulo VARCHAR2(50) NOT NULL ,
    tipo VARCHAR2(20) CHECK ( tipo IN ('opinión', 'información', 'análisis') ),
    revista NUMBER,
    numero NUMBER,
    periodista_contratado NUMBER,
    periodista_freelance NUMBER,
    CHECK (
        ((periodista_contratado IS NOT NULL) AND (periodista_freelance IS NULL)) OR
        ((periodista_contratado IS NULL) AND (periodista_freelance IS NOT NULL))
    ),
    CHECK (
        ((revista IS NULL) AND (numero IS NULL)) OR
        ((revista IS NOT NULL) AND (numero IS NOT NULL))
    )
);

-- Crear la tabla CONTRATADO
CREATE TABLE CONTRATADO (
    dni NUMBER PRIMARY KEY ,
    nombre VARCHAR2(50) NOT NULL,
    email VARCHAR2(50) UNIQUE NOT NULL ,
    sueldo NUMBER(10, 2) CHECK ( sueldo > 0 ),
    fecha_contratado DATE,
    revista NUMBER,
    tutor NUMBER,
    CHECK ( dni <> tutor ) -- No puede tutelarse a si mismo
);

-- Crear la tabla FREELANCE
CREATE TABLE FREELANCE (
    dni NUMBER PRIMARY KEY ,
    nombre VARCHAR2(50) NOT NULL ,
    email VARCHAR2(50) UNIQUE NOT NULL
);

-- Crear la tabla COLABORACION
CREATE TABLE COLABORACION (
    revista NUMBER,
    freelance NUMBER,
    pago_articulo NUMBER(10, 2) CHECK ( pago_articulo > 0 ),
    PRIMARY KEY (revista, freelance)

);

-- Crear la tabla ESPECIALIDAD_FREELANCE
CREATE TABLE ESPECIALIDAD_FREELANCE (
    freelance NUMBER,
    especialidad VARCHAR2(50),
    PRIMARY KEY (freelance, especialidad)
);

-- Alteración de las tablas para añadir las restricciones FK
ALTER TABLE REVISTA
    ADD CONSTRAINT fk_coordinador FOREIGN KEY (coordinador) REFERENCES CONTRATADO(dni);

ALTER TABLE NUMERO
    ADD CONSTRAINT fk_revista FOREIGN KEY (revista) REFERENCES REVISTA(idrev)
    ON DELETE CASCADE;

ALTER TABLE ARTICULO ADD ( 
        CONSTRAINT fk_revista_numero FOREIGN KEY (revista, numero) REFERENCES NUMERO(revista, numero),
        CONSTRAINT fk_contratado FOREIGN KEY (periodista_contratado) REFERENCES CONTRATADO(dni),
        CONSTRAINT fk_freelance FOREIGN KEY (periodista_freelance) REFERENCES FREELANCE(dni)
    );

ALTER TABLE CONTRATADO ADD (
        CONSTRAINT fk_revista_contratado FOREIGN KEY (revista) REFERENCES REVISTA(idrev),
        CONSTRAINT fk_tutor_revista FOREIGN KEY (tutor) REFERENCES CONTRATADO(dni)
    );

ALTER TABLE COLABORACION ADD (
        CONSTRAINT fk_revista_colaboracion FOREIGN KEY (revista) REFERENCES REVISTA(idrev),
        CONSTRAINT fk_freelance_colaboracion FOREIGN KEY (freelance) REFERENCES FREELANCE(dni)
    );
    
ALTER TABLE ESPECIALIDAD_FREELANCE
    ADD CONSTRAINT fk_especilidad_freelance FOREIGN KEY (freelance) REFERENCES FREELANCE(dni)
    ON DELETE CASCADE;
    
-- Insertar filas de prueba
INSERT INTO REVISTA (idrev, nombre, web, tema, periodicidad, coordinador) VALUES (1, 'Revista Tech', 'www.revistatech.com', 'Tecnología', 'Mensual', NULL);
INSERT INTO CONTRATADO (dni, nombre, email, sueldo, fecha_contratado, revista, tutor) VALUES (101, 'Juan Pérez', 'juan.perez@example.com', 3000.00, TO_DATE('2022-01-15', 'YYYY-MM-DD'), 1, NULL);
INSERT INTO FREELANCE (dni, nombre, email) VALUES (201, 'Ana López', 'ana.lopez@example.com');
INSERT INTO NUMERO (numero, fecha, num_articulos, revista) VALUES (1, TO_DATE('2024-01-01', 'YYYY-MM-DD'), 5, 1);
INSERT INTO ARTICULO (idart, titulo, tipo, revista, numero, periodista_contratado, periodista_freelance) VALUES (301, 'Innovación en IA', 'información', 1, 1, 101, NULL);
INSERT INTO COLABORACION (revista, freelance, pago_articulo) VALUES (1, 201, 150.00);
INSERT INTO ESPECIALIDAD_FREELANCE (freelance, especialidad) VALUES (201, 'Tecnología');

-- Mostrar las tablas para ver que todo se ha añadido correctamente
SELECT * FROM REVISTA;
SELECT * FROM NUMERO;
SELECT * FROM COLABORACION;
SELECT * FROM CONTRATADO;
SELECT * FROM FREELANCE;
SELECT * FROM ESPECIALIDAD_FREELANCE;