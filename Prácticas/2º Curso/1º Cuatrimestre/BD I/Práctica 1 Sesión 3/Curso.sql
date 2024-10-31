DROP TABLE CURSO CASCADE CONSTRAINTS ;
DROP TABLE INSTRUCTOR CASCADE CONSTRAINTS ;
DROP TABLE SUSCRIPTOR CASCADE CONSTRAINTS ;
DROP TABLE INSCRIPCION CASCADE CONSTRAINTS ;
DROP TABLE ESPECIALIDAD_INSTRUCTOR CASCADE CONSTRAINTS ;


CREATE TABLE CURSO (
    id_curso NUMBER PRIMARY KEY ,
    nombre VARCHAR2(50) NOT NULL,
    categoria VARCHAR2(50) CHECK ( categoria IN ('Programación', 'Diseño', 'Marketing', 'Fotografía') ),
    duracion TIMESTAMP,
    fecha_inicio DATE,
    idioma VARCHAR2(50)
);

CREATE TABLE INSTRUCTOR (
    id_instructor NUMBER PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL,
    email VARCHAR2(50) UNIQUE NOT NULL ,
    espcialidad VARCHAR2(50),
    nivel_experiencia VARCHAR2(30) CHECK ( espcialidad IN ('Principiante', 'Intermedio', 'Avanzado') )
);

CREATE TABLE SUSCRIPTOR (
  id_suscriptor NUMBER PRIMARY KEY ,
  nombre VARCHAR2(50) NOT NULL ,
  email VARCHAR2(50) UNIQUE NOT NULL,
  fecha_registro DATE
);

CREATE TABLE INSCRIPCION (
    curso NUMBER,
    suscriptor NUMBER,
    PRIMARY KEY (curso, suscriptor),
    fecha_inscripcion DATE,
    progreso NUMBER CHECK ( progreso > 0 AND progreso < 100 )
);

CREATE TABLE ESPECIALIDAD_INSTRUCTOR (
    instructor NUMBER,
    especialidad VARCHAR2(50),
    PRIMARY KEY (instructor, especialidad)
);

ALTER TABLE INSCRIPCION ADD(
    CONSTRAINT fk_inscripcion FOREIGN KEY (curso) REFERENCES CURSO(id_curso)
    ON DELETE CASCADE,
    CONSTRAINT fk_suscriptor FOREIGN KEY (suscriptor) REFERENCES SUSCRIPTOR(id_suscriptor)
    ON DELETE CASCADE,
    );

ALTER TABLE ESPECIALIDAD_INSTRUCTOR ADD (
    CONSTRAINT fk_instructor FOREIGN KEY (instructor) REFERENCES INSTRUCTOR(id_instructor)
    ON DELETE CASCADE
    );

-- Relación de exclusividad entre INSTRUCTOR y SUSCRIPTOR
ALTER TABLE INSTRUCTOR
ADD CONSTRAINT chk_email CHECK ( INSTRUCTOR.email <> SUSCRIPTOR.email );



