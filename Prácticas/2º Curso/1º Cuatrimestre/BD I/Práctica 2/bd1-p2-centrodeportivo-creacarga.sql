/*****************************************************
Sentencias de creacion de las tablas del esquema 
CENTRODEPORTIVO y de introduccion de datos
******************************************************/

-- Eliminacion de las tablas
-- La primera vez que se ejecuta da error (normal)
DROP TABLE sesion;
DROP TABLE especialista;
DROP TABLE actividad;
DROP TABLE monitor;
DROP TABLE instalacion;

-- Creacion de las tablas 

CREATE TABLE instalacion (
  instalacion_id CHAR(3)     NOT NULL,
  nombre         VARCHAR(30) NOT NULL,
  tipo           CHAR(8)     DEFAULT 'Interior' NOT NULL,
  m2             NUMBER(7,2) NOT NULL,
  CONSTRAINT instalacion_pk PRIMARY KEY(instalacion_id),
  CONSTRAINT tipo_check CHECK (tipo IN ('Interior', 'Exterior')),
  CONSTRAINT m2_check   CHECK (m2>0)
);

CREATE TABLE monitor (
  dni       CHAR(9)     NOT NULL,
  nombre    VARCHAR(30) NOT NULL,
  telefono  NUMBER(9)   NOT NULL,
  fcontrato DATE        NOT NULL,  
  salario   NUMBER(6,2) NOT NULL,
  CONSTRAINT monitor_pk PRIMARY KEY(dni),
  CONSTRAINT monitor_ak UNIQUE(telefono),
  CONSTRAINT salario_check CHECK (salario>0)
);

CREATE TABLE actividad (
  actividad_id   CHAR(3)     NOT NULL,
  nombre         VARCHAR(30) NOT NULL,
  nivel          CHAR(8)     DEFAULT 3 NOT NULL,
  precio         NUMBER(4,2) NULL,
  responsable    CHAR(9)     NOT NULL,
  instalacion_id CHAR(3)     NOT NULL,
  CONSTRAINT actividad_pk PRIMARY KEY(actividad_id),
  CONSTRAINT actividad_fk_monitor
    FOREIGN KEY(responsable)
    REFERENCES monitor(dni),
    -- ON DELETE NO ACTION ON UPDATE CASCADE
  CONSTRAINT actividad_fk_instalacion 
    FOREIGN KEY(instalacion_id)
    REFERENCES instalacion(instalacion_id),
    -- ON DELETE NO ACTION ON UPDATE CASCADE
  CONSTRAINT nivel_check  CHECK (nivel BETWEEN 1 AND 5),
  CONSTRAINT precio_check CHECK (precio IS NULL OR precio>=0)
);

CREATE TABLE especialista (
  monitor_id   CHAR(9)     NOT NULL,
  actividad_id CHAR(3)     NOT NULL,
  CONSTRAINT especialista_pk PRIMARY KEY(monitor_id, actividad_id),
  CONSTRAINT especialista_fk_monitor 
    FOREIGN KEY(monitor_id)
    REFERENCES monitor(dni),
    -- ON DELETE CASCADE ON UPDATE CASCADE
  CONSTRAINT especialista_fk_actividad 
    FOREIGN KEY(actividad_id)
    REFERENCES actividad(actividad_id)
    -- ON DELETE NO ACTION ON UPDATE CASCADE
);

CREATE TABLE sesion (
  actividad_id CHAR(3)     NOT NULL,
  diasemana    CHAR(1)     NOT NULL,
  hora         NUMBER(4,2) NOT NULL,
  monitor_id   CHAR(9)     NOT NULL,
  CONSTRAINT sesion_pk PRIMARY KEY(actividad_id, diasemana, hora),
  CONSTRAINT sesion_fk_actividad 
    FOREIGN KEY(actividad_id)
    REFERENCES actividad(actividad_id),
    -- ON DELETE CASCADE ON UPDATE CASCADE
  CONSTRAINT sesion_fk_monitor FOREIGN KEY(monitor_id)
    REFERENCES monitor(dni),
    -- ON DELETE NO ACTION ON UPDATE CASCADE
  CONSTRAINT diasemana_check  
    CHECK (diasemana IN ('L', 'M', 'X', 'J', 'V', 'S'))
);

/*********************************************************** 
Insercion de datos en las tablas del esquema CENTRODEPORTIVO
***********************************************************/
DELETE FROM sesion;
DELETE FROM especialista;
DELETE FROM actividad;
DELETE FROM monitor;
DELETE FROM instalacion;

-- instalaciones
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I01', 'Pistas de padel', 'Exterior', 600);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I02', 'Campo de futbol', 'Exterior', 8000); 
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I03', 'Sala hapkido', 'Interior', 20);  
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I04', 'Sala fitness', 'Interior', 25);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I05', 'Piscina', 'Interior', 1250);  
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I06', 'Tenis tierra batida', 'Exterior', 1050);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I07', 'Gimnasio', 'Interior', 450);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I08', 'Pabellon polideportivo', 'Interior', 1750);  
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I09', 'Sala polivalente', 'Interior', 225);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I10', 'Fronton', 'Exterior', 550);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I11', 'Cafeteria', 'Interior', 420);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I12', 'Oficinas', 'Interior', 45);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I13', 'Aparcamiento', 'Exterior', 2000);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I14', 'Almacen', 'Interior', 200);
INSERT INTO instalacion (instalacion_id, nombre, tipo, m2)
  VALUES ('I15', 'Ludoteca infantil', 'Interior', 120);  
  
-- monitores
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('11111111A', 'Filiberto', 555000111, TO_DATE('22/02/2012', 'DD/MM/YYYY'), 1620.50);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('22222222B', 'Sorentina', 555000222, TO_DATE('26/08/2002', 'DD/MM/YYYY'), 1690.30);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('33333333C', 'Exuperia', 555000333, TO_DATE('30/05/2021', 'DD/MM/YYYY'), 1000.50);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('44444444D', 'Recaredo', 555000444, TO_DATE('18/07/2013', 'DD/MM/YYYY'), 930);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('55555555E', 'Turiliano', 555000555, TO_DATE('30/10/2010', 'DD/MM/YYYY'), 1320.50);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('66666666F', 'Belinda', 555000666, TO_DATE('04/09/2005', 'DD/MM/YYYY'), 1610.50);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('77777777G', 'Pantaleon', 555000777, TO_DATE('28/04/2021', 'DD/MM/YYYY'), 1000.50);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('88888888H', 'Ursicia', 555000888, TO_DATE('16/01/2013', 'DD/MM/YYYY'), 910);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('99999999I', 'Teolindo', 555000999, TO_DATE('03/11/2022', 'DD/MM/YYYY'), 960.50);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('11223344J', 'Auspicia', 555000112, TO_DATE('10/12/1999', 'DD/MM/YYYY'), 1700.30);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('22334455K', 'Abencio', 555000223, TO_DATE('15/09/2021', 'DD/MM/YYYY'), 1000.50);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('33445566L', 'Eutiquio', 555000334, TO_DATE('23/03/2023', 'DD/MM/YYYY'), 910);
INSERT INTO monitor (dni, nombre, telefono, fcontrato, salario)
  VALUES ('44556677M', 'Leovigilda', 555000445, TO_DATE('29/09/2020', 'DD/MM/YYYY'), 910);

-- actividades
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A01', 'Pilates', 2, 15, '66666666F', 'I04');
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A02', 'Yoga', 3, 12, '11223344J', 'I04');
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A03', 'GAP', 5, 10, '55555555E', 'I04');

INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A04', 'Padel iniciacion', 2, 11, '22334455K', 'I01');  
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A05', 'Padel profesional', 2, 10, '22334455K', 'I01'); 
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A06', 'Padel grupo', 3, 8.75, '33333333C', 'I01'); 

INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A07', 'Futbol iniciacion', 3, 10, '44444444D', 'I02');
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A08', 'Futbol tecnica', 4, 15, '44444444D', 'I02');
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A09', 'Futbol perfeccionamiento', 4, 17, '44444444D', 'I02');

INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A10', 'Hapkido', 2, 9, '66666666F', 'I03');
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A11', 'Karate', 3, 9.50, '66666666F', 'I03');
  
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A12', 'Natacion iniciacion', 3, 8, '11223344J', 'I05'); 
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A13', 'Natacion perfeccionamiento', 4, 8, '11223344J', 'I05'); 
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A14', 'Aquatraining', 4, 8, '11223344J', 'I05'); 

INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A15', 'Tenis individual', 5, 15, '22334455K', 'I06'); 
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A16', 'Tenis dobles', 4, 11.50, '22334455K', 'I06');   

INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A17', 'Spinning', 5, 15, '11223344J', 'I07');   
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A18', 'Body combat', 5, 12.50, '11223344J', 'I07');   

INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A19', 'Gimnasia ritmica', 4, 7.25, '88888888H', 'I08');
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A20', 'Balonmano', 4, 7, '22222222B', 'I08');

INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A21', 'Fronton individual', 3, 8, '22334455K', 'I10');
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A22', 'Fronton dobles', 2, 5, '22334455K', 'I10');

INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A23', 'Cuentacuentos', 1, NULL, '66666666F', 'I15');

INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A24', 'Atletismo', 5, NULL, '22222222B', 'I02');
  
INSERT INTO 
  actividad (actividad_id, nombre, nivel, precio, responsable, instalacion_id)
  VALUES ('A25', 'Sauna', 1, NULL, '55555555E', 'I05');  
  
-- monitores especialistas en actividades
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('66666666F', 'A01');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('55555555E', 'A01');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A02');  
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('55555555E', 'A03');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('66666666F', 'A03');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22334455K', 'A04');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('33333333C', 'A04');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22334455K', 'A05');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('33333333C', 'A05');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('33333333C', 'A06');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22334455K', 'A06');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('44444444D', 'A07');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('44444444D', 'A08');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('88888888H', 'A08');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('44444444D', 'A09');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('77777777G', 'A09'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('66666666F', 'A10');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A10');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('66666666F', 'A11'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A12'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('99999999I', 'A12'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A13'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A14');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('66666666F', 'A14');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22334455K', 'A15');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('33333333C', 'A15');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22334455K', 'A16');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('33333333C', 'A16'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A17'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('33445566L', 'A17'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A18'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('33445566L', 'A18');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('88888888H', 'A19');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A19');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22222222B', 'A20');  
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22334455K', 'A21');  
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22334455K', 'A22');  
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A22');  
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('66666666F', 'A23'); 
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('77777777G', 'A23');

INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A11');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('99999999I', 'A13');
  
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22222222B', 'A21');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22222222B', 'A22');  
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('66666666F', 'A21'); 

INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A01');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A02');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A03');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A04');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A05');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A06');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A07');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A08');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A09');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A10');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A11');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A12');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A13');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A14');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A15');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A16');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A17');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A18');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A19');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A20');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A21');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A22');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A23');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11111111A', 'A25');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('11223344J', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22222222B', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('22334455K', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('33333333C', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('33445566L', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('44444444D', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('55555555E', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('66666666F', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('77777777G', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('88888888H', 'A24');
INSERT INTO especialista (monitor_id, actividad_id)
  VALUES ('99999999I', 'A24');
  
-- sesiones 
-- pilates
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A01', 'L', 09.15, '55555555E');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A01', 'X', 09.15, '55555555E');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A01', 'L', 19.00, '66666666F');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A01', 'M', 18.00, '55555555E');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A01', 'X', 19.00, '66666666F');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A01', 'J', 18.00, '55555555E');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A01', 'S', 10.00, '55555555E');

-- Yoga
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A02', 'M', 20.00, '11223344J');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A02', 'J', 20.00, '11223344J');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A02', 'V', 09.30, '11223344J');

-- GAP
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A03', 'L', 11.30, '55555555E');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A03', 'X', 17.15, '55555555E');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A03', 'J', 09.00, '66666666F');
  
-- Padel
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A04', 'L', 17.30, '22334455K');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A04', 'X', 17.30, '22334455K');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A05', 'M', 17.30, '33333333C');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A05', 'J', 17.30, '33333333C');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A06', 'S', 13.15, '33333333C');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id) -- nueva
  VALUES ('A06', 'S', 14.15, '33333333C');

-- Futbol 
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A07', 'M', 17.45, '44444444D');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A07', 'J', 17.45, '44444444D');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A08', 'M', 18.45, '88888888H');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A09', 'X', 19.15, '77777777G');  
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A09', 'V', 19.15, '77777777G');  

-- Hapkido 
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A10', 'L', 16.30, '11223344J');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A10', 'X', 16.30, '11223344J');
-- Karate
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A11', 'J', 12.30, '11223344J');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A11', 'S', 12.30, '11223344J');

-- Natacion
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A12', 'L', 18.15, '99999999I');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A12', 'X', 18.15, '99999999I');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A12', 'V', 18.15, '99999999I');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A13', 'M', 20.15, '99999999I');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A13', 'J', 20.15, '99999999I');

-- Aquatraining
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A14', 'M', 10.00, '66666666F');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A14', 'J', 10.00, '66666666F');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A14', 'S', 18.00, '66666666F');

-- Tenis
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A15', 'M', 19.00, '22334455K');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A15', 'J', 19.00, '22334455K');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A16', 'M', 20.30, '33333333C');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A16', 'J', 20.30, '33333333C');

-- Spinning
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A17', 'L', 12.30, '33445566L');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A17', 'M', 13.00, '33445566L');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A17', 'J', 13.00, '33445566L');

-- Body combat
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A18', 'X', 20.00, '11223344J');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A18', 'S', 09.30, '11223344J');  

-- Gimnasia ritmica
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A19', 'M', 16.45, '88888888H');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A19', 'V', 16.45, '88888888H');    

-- Balonmano
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A20', 'L', 18.30, '22222222B');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A20', 'J', 18.30, '22222222B'); 
    
-- Fronton individual y dobles  
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A21', 'L', 19.45, '22222222B');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A21', 'X', 19.45, '22222222B');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A21', 'V', 20.00, '22222222B');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id) -- nueva
  VALUES ('A22', 'S', 19.00, '22222222B');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id) 
  VALUES ('A22', 'S', 20.00, '22222222B');  
  
-- Cuentacuentos  
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A23', 'M', 18.00, '66666666F');
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A23', 'V', 18.00, '66666666F');  
INSERT INTO sesion (actividad_id, diasemana, hora, monitor_id)
  VALUES ('A23', 'S', 12.00, '66666666F'); 

-- confirmacion de los datos introducidos 
COMMIT;