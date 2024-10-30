-- Crear la Tabla departamentos
/*
Primero, crearemos la tabla 'departamentos', que contiene los datos de cada departamento.
La columna 'id_departamento' será la clave primaria
*/

CREATE TABLE departamentos (
    id_departamento INT PRIMARY KEY,
    nombre_departamento VARCHAR2(50) NOT NULL
);

/*
Explicación:
-   'id_departamento': Tipo INT, es la clave primaria (PRIMARY KEY), lo que garantiza que 
    cada valor en esta columna sea único

-   'nombre_departamento': Tupo VARCHAR2(50), con un límite de 50 caracteres, y no se 
    permite que esté vacío (NOT NULL)
*/

-- Crear la Tabla empleados
/*
Después, crearemos la tabla 'empleados'. Esta tabla tiene una columna 'id_departamento', que 
actúa como una clave foránea (FOREIGN KEY) y se refiere a la columna 'id_departamento' de la 
tabla 'departamentos'.
*/

CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL,
    salario DECIMAL(10, 2),
    id_departamento INT,
    CONSTRAINT salario_ok CHECK (salario>0),
    CONSTRAINT fk_departamento FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
);

/*
Explicación:
-   'id_empleado': Tipo INT, es la clave primaria para identificar de forma única a cada empleado.
-   'nombre': Tipo VARCHAR2(50), con un límite de 50 caracteres, y no se permite que esté 
    vacío (NOT NULL).
-   'salario': Tipo DECIMAL(10, 2) que admite hasta 10 dígito, incluyendo 2 decimales para 
    representar el salario
-   'id_departamento': Tipo INT, que es la clave foránea que se relaciona con la columna 
    'id_departamento' en la tabla 'departamentos'
-   La restricción 'CONSTRAINT fk_departamento FOREING KEY' asegura que cada valor de 
    'id_departamento' en la tabla 'empleados' corresponda a un valor en la tabla
    'departamentos'.
*/

-- Ejemplo de Insertar Datos
-- Insertar datos en la tabla departamentos
INSERT INTO departamentos (id_departamento, nombre_departamento) VALUES (1, 'Ventas');
INSERT INTO departamentos (id_departamento, nombre_departamento) VALUES (2, 'Finanzas');
INSERT INTO departamentos (id_departamento, nombre_departamento) VALUES (3, 'Recursos Humanos');

-- Insertar datos en la tabla empleados
INSERT INTO empleados (id_empleado, nombre, salario, id_departamento) VALUES (1, 'Juan Zapata', 1500.00, 1);
INSERT INTO empleados (id_empleado, nombre, salario, id_departamento) VALUES (2, 'Jose Carlos Sanchez', 1320.20, 2);
INSERT INTO empleados (id_empleado, nombre, salario, id_departamento) VALUES (3, 'Francisco Javier Mercader', 2000.00, 3);

SELECT * FROM empleados;
SELECT * FROM departamentos;

-- Primero eliminamos la tabla 'empleados' para evitar conflictos con FK
-- DROP TABLE empleados;

-- Luego eliminamos la tabla 'departamento'
-- DROP TABLE departamentos;
