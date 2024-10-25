/*
Consultas que acceden a las tablas del esquema de Clientes y Cuentas
Forma parte del TUTORIAL de SQL Developer.
*/

-- Todas las cuentas
SELECT * 
FROM CUENTA;

-- Todos los clientes
SELECT * 
FROM CLIENTE;

-- Clientes de Murcia
-- Lo encerrado entre comillas simples es un literal y distingue mayusculas/minusculas. 
SELECT *
FROM CLIENTE
WHERE ciudad = 'Murcia';

-- Nombre, direccion y ciudad de clientes que NO viven en Murcia
SELECT nombre, direccion, ciudad
FROM CLIENTE
WHERE ciudad != 'Murcia'; -- Tambien valdria <>

-- Codigo y nombre del cliente titular de cada cuenta
SELECT Q.numero, C.codigo, C.nombre 
FROM CLIENTE C JOIN CUENTA Q ON (C.codigo = Q.cliente);

-- Otra manera de resolver la misma consulta
SELECT Q.numero, C.codigo, C.nombre 
FROM CLIENTE C, CUENTA Q 
WHERE C.codigo = Q.cliente;

-- Nombre de los clientes autorizados en la cuenta 505.
SELECT nombre
FROM CLIENTE
WHERE codigo IN
    (SELECT cliente
     FROM AUTORIZADO
     WHERE cuenta = 505);
	 
-- Visualizacion de los datos a traves de la vista
SELECT *
FROM TITULAR_DE_CUENTA;
