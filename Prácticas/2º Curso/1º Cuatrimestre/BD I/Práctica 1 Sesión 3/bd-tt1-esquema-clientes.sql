-- Tablas para el TUTORIAL de SQL Developer

/*
 *** Realizacion del tutorial con un PC propio ***
 Este script debe ser ejecutado por una cuenta de usuario no administrador 

 *** Realizacion del tutorial con un PC de un laboratorio FIUM ***
 En el Servidor Oracle este script ya ha sido ejecutado por el usuario BDG0000
 
  NO EJECUTAR. NO EJECUTAR. NO EJECUTAR. NO EJECUTAR. NO EJECUTAR.
*/

-- Creacion de tablas del esquema CUENTASYCLIENTES

CREATE TABLE CLIENTE (
   codigo    CHAR(4)     PRIMARY KEY,
   nombre    VARCHAR(20) NOT NULL,
   direccion VARCHAR(20),
   ciudad    VARCHAR(20)
   );

CREATE TABLE CUENTA (
   numero  NUMBER(5)   PRIMARY KEY, 
   saldo   NUMBER(7,2) NOT NULL,
   cliente CHAR(4)     NOT NULL,
   FOREIGN KEY (cliente) REFERENCES CLIENTE(codigo)
                         ON DELETE CASCADE,
   CONSTRAINT cuenta_saldo_ok CHECK (saldo>=0)
   );

CREATE TABLE AUTORIZADO (
  cuenta  NUMBER(5),
  cliente CHAR(4),
  PRIMARY KEY (cuenta, cliente),
  FOREIGN KEY (cliente) REFERENCES CLIENTE(codigo),
  FOREIGN KEY (cuenta)  REFERENCES CUENTA(numero)
                        ON DELETE CASCADE
);

-- Creacion de una vista

CREATE VIEW TITULAR_DE_CUENTA
AS SELECT numero cuenta, nombre nombre_titular
   FROM CUENTA, CLIENTE 
   WHERE cliente=codigo
   ORDER BY numero DESC;

-- Introduccion de datos en las tablas.
-- Observe que las cadenas de caracteres necesitan comillas simples.
   
INSERT INTO CLIENTE VALUES ('C210', 'Garcia, A.', 'Gran Via, 6', 'Murcia');
INSERT INTO CLIENTE VALUES ('C300', 'Lopez, B.', 'Ronda Norte, 3', 'Murcia');
INSERT INTO CLIENTE VALUES ('C003', 'Azorin, C.', 'Paseo Rosales, 9', 'Molina');
INSERT INTO CLIENTE VALUES ('C689', 'Perez, D.', 'Plaza Mayor, 2', 'Cieza');
INSERT INTO CLIENTE VALUES ('C333', 'Gomez, F.', 'Ronda Este, 6', 'Patino');
INSERT INTO CLIENTE VALUES ('C220', 'Sanchez, E.', 'Costera baja, 5', 'Aljucer');
INSERT INTO CLIENTE VALUES ('C100', 'Hita, G.', 'Plaza Chica, 7', 'Casillas');


INSERT INTO CUENTA VALUES(200, 85005, 'C689');
INSERT INTO CUENTA VALUES(505, 40000, 'C003');
INSERT INTO CUENTA VALUES(821, 50000, 'C210');
INSERT INTO CUENTA VALUES(426, 35620, 'C003');
INSERT INTO CUENTA VALUES(105, 29872, 'C300');

INSERT INTO AUTORIZADO(cuenta, cliente) VALUES(505, 'C220');
INSERT INTO AUTORIZADO(cuenta, cliente) VALUES(505, 'C300');
INSERT INTO AUTORIZADO(cuenta, cliente) VALUES(821, 'C100');
INSERT INTO AUTORIZADO(cuenta, cliente) VALUES(505, 'C333');

-- Confirmacion de los datos introducidos: los hace permanentes.
COMMIT;