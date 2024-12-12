/*
Asignatura: Bases de Datos I
Curso académico: 2024/25
Convocatoria: Enero
P3. Definición y modificación de datos en SQL
Autores:
- Francisco Javier Mercader Martínez
- Pedro Alarcón Fuentes
*/

-- Sentencias INSERT
-- REVISTAS
ALTER TABLE revista DISABLE CONSTRAINT coordinador_fk_contratado;

INSERT INTO REVISTA(idrev, nombre, tema, web, periodicidad, coordinador) 
  VALUES ('R01', 'NATURALIZA', 'NATURALEZA', NULL, 'Mensual', '11223344P');

INSERT INTO REVISTA(idrev, nombre, tema, web, periodicidad, coordinador) 
  VALUES ('R02', 'FUENTE PRIMARIA', 'POLITICA', 'fuenteprimaria.com', 
          'Semanal', '44556677A');
INSERT INTO REVISTA(idrev, nombre, tema, web, periodicidad, coordinador) 
  VALUES ('R03', 'VIAJAR HOY', 'VIAJES', NULL, 'Trimestral', '66778899J');
INSERT INTO REVISTA(idrev, nombre, tema, web, periodicidad, coordinador) 
  VALUES ('R04', 'TECNOFIUM', 'TECNOLOGIA', 'tecnofium.um.es', 
          'Mensual', '55667788M');


-- PERIODISTAS CONTRATADOS
ALTER TABLE contratado DISABLE CONSTRAINT contratado_fk_revista;
INSERT INTO 
 CONTRATADO (DNI, nombre, email, sueldo, revista, fecha_contrato, tutor) 
 VALUES ('11223344P', 'PEPA BUENO', 'pbueno@mail.com', 1050.5, 'R01',
         TO_DATE('01/01/2001', 'dd/mm/yyyy'), NULL); -- sin tutor
INSERT INTO 
 CONTRATADO (DNI, nombre, email, sueldo, revista, fecha_contrato, tutor) 
 VALUES ('44556677A', 'ANA PASTOR', 'apastor@mail.com', 2000, 'R02', 
         TO_DATE('04/04/2004', 'dd/mm/yyyy'), NULL); -- sin tutor
INSERT INTO 
 CONTRATADO (DNI, nombre, email, sueldo, revista, fecha_contrato, tutor) 
 VALUES ('55667788M', 'MARIA GONZALEZ', 'mgonzalez@mail.com', 2150.5, 'R04', 
         TO_DATE('05/05/2014', 'dd/mm/yyyy'), NULL); -- sin tutor
INSERT INTO 
 CONTRATADO (DNI, nombre, email, sueldo, revista, fecha_contrato, tutor) 
 VALUES ('66778899J', 'JULIA OTERO', 'jotero@mail.com', 1100.5, 'R03', 
         TO_DATE('06/06/1999', 'dd/mm/yyyy'), NULL); -- sin tutor 
INSERT INTO 
 CONTRATADO (DNI, nombre, email, sueldo, revista, fecha_contrato, tutor) 
 VALUES ('33445566M', 'MAMEN MENDIZABAL', 'mmendizabal@mail.com', 1505, 'R02', 
         TO_DATE('03/03/2003', 'dd/mm/yyyy'), '44556677A'); 

INSERT INTO 
 CONTRATADO (DNI, nombre, email, sueldo, revista, fecha_contrato, tutor) 
 VALUES ('22334455A', 'AIMAR BRETOS', 'abretos@mail.com', 1230, 'R01', 
         TO_DATE('02/02/2002','dd/mm/yyyy'), '11223344P');
INSERT INTO 
 CONTRATADO (DNI, nombre, email, sueldo, revista, fecha_contrato, tutor) 
 VALUES ('77889900L', 'LAURA CAMACHO', 'lcamacho@mail.com', 1500.0, 'R04', 
         TO_DATE('07/07/2018', 'dd/mm/yyyy'), '55667788M'); 
INSERT INTO 
 CONTRATADO (DNI, nombre, email, sueldo, revista, fecha_contrato, tutor) 
 VALUES ('88990011J', 'JORDI PEREZ', 'jperez@mail.com', 1375.5, 'R04', 
         TO_DATE('07/07/2017', 'dd/mm/yyyy'), '77889900L'); 

INSERT INTO 
 CONTRATADO (DNI, nombre, email, sueldo, revista, fecha_contrato, tutor) 
 VALUES ('00112233S', 'SILVIA INTXAURRONDO', 'sintxa@mail.com', 2000, 'R02', 
         TO_DATE('29/08/2013', 'dd/mm/yyyy'), '44556677A'); 
ALTER TABLE contratado ENABLE CONSTRAINT contratado_fk_tutor;
ALTER TABLE revista ENABLE CONSTRAINT coordinador_fk_contratado;

-- PERIODISTAS FREELANCE

INSERT INTO FREELANCE (DNI, nombre, email) 
  VALUES ('01234567G', 'JOSEFINA CARABIAS', 'jcarabias@mail.com');
INSERT INTO FREELANCE (DNI, nombre, email) 
  VALUES ('12345678A', 'ANTONIO PAMPLIEGA', 'apampliega@mail.com');
INSERT INTO FREELANCE (DNI, nombre, email) 
  VALUES ('23456789G', 'XAVIER ALDEKOA', 'xaldekoa@mail.com');
INSERT INTO FREELANCE (DNI, nombre, email) 
  VALUES ('45678901J', 'JON SISTIAGA', 'jsistiaga@mail.com');
INSERT INTO FREELANCE (DNI, nombre, email) 
  VALUES ('78901234R', 'ROSA MARIA CALAF','rcalaf@mail.com');

-- COLABORACIONES entre freelances y revistas

INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('12345678A', 'R01', 100);
INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('12345678A', 'R02', 120);

INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('45678901J', 'R01', 200);
INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('45678901J', 'R03', 250);

INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('78901234R', 'R01', 400);
INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('78901234R', 'R02', 450);
INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('78901234R', 'R03', 475);

INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('01234567G', 'R01', 500);
INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('01234567G', 'R02', 550);
INSERT INTO COLABORACION (freelance, revista, pago_articulo)
  VALUES ('01234567G', 'R03', 575);


-- NUMEROS DE REVISTA
-- Se pone un 0 en la columna num_articulos, que se calcula al final

-- numeros de revista R01 NATURALIZA Mensual
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R01', 1, TO_DATE('01/01/2024', 'dd/mm/yyyy'), 0);
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R01', 2, TO_DATE('01/02/2024', 'dd/mm/yyyy'), 0);
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R01', 3, TO_DATE('01/03/2024', 'dd/mm/yyyy'), 0);

-- numeros de revista R02 semanal
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R02', 1, TO_DATE('06/03/2024', 'dd/mm/yyyy'), 0);
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R02', 2, TO_DATE('13/03/2024', 'dd/mm/yyyy'), 0);
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R02', 3, TO_DATE('20/03/2024', 'dd/mm/yyyy'), 0);
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R02', 4, TO_DATE('27/03/2024', 'dd/mm/yyyy'), 0);
  
-- numeros de revista R03 trimestral
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R03', 1, TO_DATE('15/12/2023', 'dd/mm/yyyy'), 0);
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R03', 2, TO_DATE('15/03/2024', 'dd/mm/yyyy'), 0);

-- numeros de revista R04 Mensual
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R04', 1, TO_DATE('14/11/2023', 'dd/mm/yyyy'), 0);
INSERT INTO NUMERO (revista, numero, fecha, num_articulos) 
  VALUES ('R04', 2, TO_DATE('14/12/2023', 'dd/mm/yyyy'), 0);

-- ARTICULOS 

-- articulos de la revista R03 
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A001', 'RUTA POR EL OKAVANGO', 'Informacion', NULL, '01234567G', 
          'R03', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A002', 'FALSOS GUIAS DE VIAJE', 'Analisis', NULL, '78901234R', 
          'R03', 1);          
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A003', 'PERDIDO EN ZAMBIA', 'Informacion', '66778899J', NULL, 
          'R03', 1);          
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A004', 'ALEMANIA EN PRIMAVERA', 'Informacion', NULL, '78901234R', 
          'R03', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A005', 'BRASIL DESCONOCIDO', 'Analisis', '66778899J', NULL,
          'R03', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A006', 'APOYO A SOMALIA', 'Informacion', NULL, '01234567G',
          'R03', 2); 
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A007', 'HIJOS DEL NILO', 'Analisis', NULL, '01234567G',
          'R03', 2);          
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A008', 'RUTAS POR ISLANDIA', 'Informacion', NULL, '45678901J',
          'R03', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A009', 'RUTAS POR EL LONDRES SOLIDARIO', 'Informacion', NULL, 
          '78901234R', 'R03', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A010', 'SER DENTISTA EN AFRICA', 'Analisis', NULL, '01234567G',
          'R03', 2);
          
-- articulos de la revista R02
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A011', 'DEBATE ELECTORAL', 'Analisis', '44556677A', NULL,
          'R02', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A012', 'POLEMICAS INVENTADAS', 'Opinion', '33445566M', NULL, 
          'R02', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A013', 'CONFERENCIA DE PRESIDENTES EUROPEOS', 'Analisis', NULL, 
          '01234567G', 'R02', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A014', 'LAS TERTULIAS EN TV COMO ARMA ELECTORAL', 'Opinion',
          '44556677A', NULL, 'R02', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A015', 'DESInformacion POLITICA', 'Opinion', '44556677A', NULL, 
          'R02', 2);   
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A016', 'CONFLICTOS OLVIDADOS', 'Informacion', NULL, '12345678A', 
          'R02', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A017', 'LA GUERRA MAS LARGA', 'Informacion', NULL, '12345678A',
          'R02', 3);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A018', 'ACUERDOS DIPLOMATICOS EUROPA-JAPON', 'Analisis', NULL, 
          '78901234R', 'R02', 4);  
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A019', 'PROMESAS ELECTORALES INCUMPLIDAS', 'Informacion', 
          '33445566M', NULL, 'R02', 4);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A020', 'CONFLICTOS ARMADOS SILENCIADOS', 'Analisis', NULL, 
          '12345678A', 'R02', 3);  
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A021', 'FAKE NEWS', 'Analisis', '44556677A', NULL, 
          'R02', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A022', 'UN DIA CON EL PRESIDENTE', 'Opinion', '33445566M', NULL,
          'R02', 4);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A023', 'DIALOGOS DE BESUGOS', 'Analisis', '44556677A', NULL, 
          'R02', 2);

-- Articulos de la revista R01
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A024', 'LA RAPAZ GIGANTE DE LA AMAZONIA', 'Informacion', NULL, 
           '78901234R', 'R01', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A025', 'LA REGENERACION DE PORTMAN', 'Informacion', NULL, '01234567G',
          'R01', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A026', 'QUE SON LAS TECNOLOGIAS VERDES', 'Informacion', NULL,
          '78901234R', 'R01', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A027', 'NATURALISMO VS ECOLOGISMO', 'Opinion', NULL, '45678901J',
          'R01', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A028', 'DESCUBRE LAS ISLAS MAURICIO', 'Informacion', NULL, 
          '78901234R', 'R01', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A029', 'QUE PASARIA SI SE EXTINGUIERAN LAS ABEJAS', 'Analisis', 
          NULL, '01234567G', 'R01', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A030', 'TOXICOS EN EL AGUA', 'Informacion', '11223344P', NULL, 
          'R01', 3); 
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A031', 'RECUPERAR EL SUELO AGRARIO', 'Informacion', '22334455A', NULL, 
          'R01', 3);           
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A032', 'DIA MUNDIAL DEL AGUA', 'Informacion', '22334455A', NULL, 
          'R01', 3);           

-- articulos de la revista R04       
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A033', 'LANZAMIENTO DE RETURN TO MONKEY ISLAND', 'Opinion', 
          '55667788M', NULL, 'R04', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A034', 'POKEMON GO FEST 2024', 'Analisis', '55667788M', NULL,
          'R04', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A035', 'GUERRA TECNOLOGICA', 'Analisis', '77889900L', NULL, 
          'R04', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A036', 'FORNITE: SKINS BASADAS EN ASSASSINS CREED', 'Informacion', 
          '55667788M', NULL, 'R04', 2);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A037', 'MALWARE EN GOOGLE PLAY', 'Informacion', '77889900L', NULL, 
          'R04', 1);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A038', 'LOS MEJORES MOODS DE ELDEN RING', 'Analisis', 
          '55667788M', NULL, 'R04', 2);

INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A039', 'CIBERATAQUE EN IBERDROLA', 'Informacion', '77889900L', NULL,  
          NULL, NULL);

INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A040', 'EL MAYOR ROBO DE CRIPTOMONEDA DE LA HISTORIA', 'Informacion',
          '77889900L', NULL, 'R04', 2);          
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A041', 'TELEFONICA MIGRA SUS BASES DE DATOS A LA NUBE DE ORACLE',
          'Informacion', '88990011J', NULL, NULL, NULL);
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A042', 'EL 30% DE LAS EMPRESAS NO TIENE UNA ESTRATEGIA CLOUD',
          'Informacion', '88990011J', NULL, 'R04', 2);          
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A043', 'VIAJAR CON SENTIDO COMUN', 'Informacion', '66778899J', NULL,
          NULL, NULL);   
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A044', 'PAC-MAN REVISITED', 'Informacion', '55667788M', NULL,
          NULL, NULL);  
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A045', 'COMO PROTEGER TU MOVIL', 'Informacion', '77889900L', NULL,  
          'R04', 2);          
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A046', 'EL SUENNO DE AFRICA', 'Analisis', NULL, '01234567G',
          'R03', 2);   
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A047', 'SALVAJE', 'Analisis','66778899J', NULL, 
          'R03', 2); 
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A048', 'EN LAS ANTIPODAS', 'Analisis', NULL, '45678901J',
          'R03', 2); 
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A049', 'LA IA QUE ARRASA POR DONDE PASA', 'Opinion', NULL, '45678901J',
          'R04', 2); 
INSERT INTO
  ARTICULO (idart, titulo, tipo, contratado, freelance, revista, numero)
  VALUES ('A050', 'BULOS Y ANTI-INFORMACION', 'Analisis', NULL, '01234567G',
          'R02', 2); 

-- UPDATE columna calculada
UPDATE NUMERO N SET num_articulos= (SELECT COUNT(*) 
                                    FROM ARTICULO A
                                    WHERE A.revista = N.revista 
                                      AND A.numero = N.numero);
COMMIT;