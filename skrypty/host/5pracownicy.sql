create table robert.pracownicy(
emp_id int NOT NULL,
imie varchar(50) NOT NULL,
nazwisko varchar(50) NOT NULL,
pesel number(11) NOT NULL UNIQUE,
stanowisko varchar(50) NOT NULL,
wynagrodzenie number(9,2) NOT NULL,
PRIMARY KEY (emp_id)
);

ALTER TABLE robert.pracownicy
ADD CHECK (wynagrodzenie>=0 and pesel>=0);

CREATE SEQUENCE robert.emp_seq
MINVALUE 0
START WITH 0
INCREMENT BY 2
CACHE 10;

CREATE OR REPLACE TRIGGER robert.pracownicy_inc 
BEFORE INSERT ON robert.pracownicy 
FOR EACH ROW
WHEN (new.emp_id IS NULL)
BEGIN
  SELECT robert.emp_seq.NEXTVAL
  INTO   :new.emp_id
  FROM   dual;
END;
/


CREATE OR REPLACE PROCEDURE robert.dodaj_pracownika
(imie_ IN varchar,
nazwisko_ IN varchar,
pesel_ IN number,
stanowisko_ IN varchar,
wynagrodzenie_ IN number
)
AS
BEGIN
  INSERT INTO ROBERT.pracownicy(imie, nazwisko,pesel,stanowisko,wynagrodzenie)
  VALUES (imie_, nazwisko_, pesel_, stanowisko_, wynagrodzenie_);
  commit;
  EXCEPTION
    WHEN others THEN
      dbms_output.put_line( 'Error! ');
      rollback;
END;
/

CREATE OR REPLACE PROCEDURE robert.usun_pracownika
(emp_id_ IN int
)
AS
numm int;
CURSOR CUR_EMP IS 
SELECT emp_id from robert.pracownicy where emp_id=emp_id_ FOR UPDATE;
BEGIN
  OPEN CUR_EMP;
  FETCH CUR_EMP into numm; 
  IF CUR_EMP%NOTFOUND THEN
    dbms_output.put_line('Error! Employee does not exist!');
    RETURN;
  END IF;
  DELETE FROM robert.pracownicy WHERE CURRENT OF CUR_EMP;
  CLOSE CUR_EMP;
  commit;
  
  EXCEPTION
    WHEN others THEN
      dbms_output.put_line( 'Error! ');
      rollback;
END;
/
