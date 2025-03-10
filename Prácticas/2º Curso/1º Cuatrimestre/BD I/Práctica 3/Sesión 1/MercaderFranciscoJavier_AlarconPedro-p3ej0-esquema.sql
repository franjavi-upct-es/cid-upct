/*
Asignatura: Bases de Datos I
Curso académico: 2024/25
Convocatoria: Enero
P3. Definición y modificación de datos en SQL
Autores:
- Francisco Javier Mercader Martínez
- Pedro Alarcón Fuentes
*/

-- Sentencia DROP para eliminar la tabla aunque tenga restricciones
DROP TABLE REVISTA CASCADE CONSTRAINTS;
DROP TABLE NUMERO CASCADE CONSTRAINTS;
DROP TABLE ARTICULO CASCADE CONSTRAINTS;
DROP TABLE CONTRATADO CASCADE CONSTRAINTS;
DROP TABLE FREELANCE CASCADE CONSTRAINTS;
DROP TABLE COLABORACION CASCADE CONSTRAINTS;
DROP TABLE ESPECIALIDAD_FREELANCE CASCADE CONSTRAINTS;

-- Sentencias CREATE (y ALTER) para crear las tablas del esquema
-- en el orden que evite errores de integridad referencial

-- Crear tabla REVISTA
CREATE TABLE REVISTA (
    idrev CHAR(3),
    nombre VARCHAR2(50) UNIQUE NOT NULL,
    web VARCHAR2(50) NULL,
    tema VARCHAR2(50) NOT NULL,
    periodicidad VARCHAR2(50) NOT NULL,
    coordinador CHAR(9) UNIQUE NOT NULL,
    CONSTRAINT periodicidad_ok CHECK (
        periodicidad IN ('Semanal', 'Quincenal', 'Mensual', 'Bimestral', 'Trimestral', 'Anual')
    ),
    CONSTRAINT pk_revista PRIMARY KEY (idrev)
);

-- Crear tabla NUMERO
CREATE TABLE NUMERO (
    numero NUMBER(4) NOT NULL,
    fecha DATE NOT NULL,
    num_articulos NUMBER NOT NULL,
    revista CHAR(3) NOT NULL,
    CONSTRAINT pk_numero PRIMARY KEY (revista, numero),
    CONSTRAINT num_articulos_ok CHECK (num_articulos >= 0),
    CONSTRAINT numero_ok CHECK (numero > 0)
);

-- Crear tabla ARTICULO
CREATE TABLE ARTICULO (
    idart CHAR(4),
    titulo VARCHAR2(60) NOT NULL,
    tipo VARCHAR2(20) NOT NULL,
    revista CHAR(3) NULL,
    numero NUMBER(4) NULL,
    contratado CHAR(9) NULL,
    freelance CHAR(9) NULL,
    CONSTRAINT pk_articulo PRIMARY KEY (idart),
    CONSTRAINT diferente_periodista CHECK (
        ((contratado IS NOT NULL) AND (freelance IS NULL)) OR
        ((contratado IS NULL) AND (freelance IS NOT NULL))
    ),
    CONSTRAINT tipo_ok CHECK (tipo IN ('Opinion', 'Informacion', 'Analisis')),
    CONSTRAINT revista_numero_ok CHECK (
    ((revista is NULL) AND (numero IS NULL)) OR ((revista IS NOT NULL) AND (numero IS NOT NULL))
    )
);

-- Crear tabla CONTRATADO
CREATE TABLE CONTRATADO (
    dni CHAR(9),
    nombre VARCHAR2(50) NOT NULL,
    email VARCHAR2(50) UNIQUE NOT NULL,
    sueldo NUMBER(10, 2) CHECK (sueldo > 0) NOT NULL,
    fecha_contrato DATE NOT NULL,
    revista CHAR(4) NOT NULL,
    tutor CHAR(9) NULL,
    CONSTRAINT pk_contratado PRIMARY KEY (dni),
    CONSTRAINT dni_diferente_a_tutor CHECK (dni <> tutor)
);

-- Crear tabla FREELANCE
CREATE TABLE FREELANCE (
    dni CHAR(9),
    nombre VARCHAR2(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    CONSTRAINT pk_freelance PRIMARY KEY (dni)
);

-- Crear tabla COLABORACION
CREATE TABLE COLABORACION(
    revista CHAR(3) NOT NULL,
    freelance CHAR(9) NOT NULL,
    pago_articulo NUMBER(10, 2) NOT NULL, 
    CONSTRAINT pk_colaboracion PRIMARY KEY (revista, freelance),
    CONSTRAINT pago_articulo_ok CHECK (pago_articulo > 0) 
);

-- Crear tabla ESPECIALIDAD_FREELANCE
CREATE TABLE ESPECIALIDAD_FREELANCE(
    freelance CHAR(9) NOT NULL,
    especialidad VARCHAR(20) NOT NULL,
    CONSTRAINT pk_especialidad_freelance PRIMARY KEY (freelance, especialidad)
);

-- Agregar las restricciones una vez est�n creadas las tablas

ALTER TABLE REVISTA 
    ADD CONSTRAINT coordinador_fk_contratado FOREIGN KEY (coordinador) REFERENCES CONTRATADO(dni);
    -- ON DELETE NO ACTION
    -- ON UPDATE CASCADE
    
ALTER TABLE NUMERO 
    ADD CONSTRAINT numero_fk_revista FOREIGN KEY (revista) REFERENCES REVISTA (idrev)
    ON DELETE CASCADE;
    -- ON UPDATE CASCADE

ALTER TABLE ARTICULO ADD (
    CONSTRAINT articulo_fk_revista_numero FOREIGN KEY (revista, numero) REFERENCES NUMERO(revista, numero),
    -- ON DELETE NO ACTION
    -- ON UPDATE CASCADE
    CONSTRAINT articulo_fk_contratado FOREIGN KEY (contratado) REFERENCES CONTRATADO(dni),
    -- ON DELETE NO ACTION
    -- ON UPDATE CASCADE
    CONSTRAINT articulo_fk_freelance FOREIGN KEY (freelance) REFERENCES FREELANCE(dni)
    -- ON DELETE NO ACTION
    -- ON UPDATE CASCADE
);

ALTER TABLE CONTRATADO ADD (
    CONSTRAINT contratado_fk_revista FOREIGN KEY (revista) REFERENCES REVISTA(idrev),
    -- ON DELETE NO ACTION
    -- ON UPDATE CASCADE
    CONSTRAINT contratado_fk_tutor FOREIGN KEY (tutor) REFERENCES CONTRATADO(dni)
    -- ON DELETE NO ACTION
    -- ON UPDATE CASCADE
);

ALTER TABLE COLABORACION ADD (
    CONSTRAINT colaboracion_fk_revista FOREIGN KEY (revista) REFERENCES REVISTA(idrev),
    -- ON DELETE NO ACTION
    -- ON UPDATE CASCADE
    CONSTRAINT colaboracion_fk_freelance FOREIGN KEY (freelance) REFERENCES FREELANCE(dni)
    -- ON DELTE NO ACTION
    -- ON UPDATE CASCADE
);

ALTER TABLE ESPECIALIDAD_FREELANCE 
    ADD CONSTRAINT especialidad_fk_freelance FOREIGN KEY (freelance) REFERENCES FREELANCE(dni)
    ON DELETE CASCADE;
    -- ON UPDATE CASCADE