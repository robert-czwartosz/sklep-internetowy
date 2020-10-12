create table robert.produkty(
product_id int NOT NULL,
nazwa varchar(100) NOT NULL UNIQUE,
ilosc int NOT NULL,
cena number(9,2) NOT NULL,
opis varchar(1024) NOT NULL,
PRIMARY KEY (product_id)
);

ALTER TABLE robert.produkty
ADD CHECK (ilosc>=0 and cena>=0);

CREATE SEQUENCE robert.product_seq
MINVALUE 0
START WITH 1
INCREMENT BY 1
CACHE 10;

CREATE OR REPLACE PROCEDURE robert.insert_product
(
nazwa_ IN varchar,
ilosc_ IN int,
cena_ IN float,
opis_ IN varchar
)
AS
BEGIN
  INSERT INTO robert.produkty@orcl
  VALUES (robert.product_seq.NEXTVAL, nazwa_, ilosc_, cena_, opis_);
  commit;
  
  EXCEPTION
    WHEN others THEN
      rollback;
      dbms_output.put_line('Error!');
END;
/

CREATE OR REPLACE PROCEDURE robert.dostawa_produktu
(
nazwa_ IN varchar,
ilosc_ IN int
)
AS
BEGIN
  UPDATE robert.produkty@orcl
  SET ilosc = ilosc + ilosc_
  WHERE nazwa=nazwa_;
  
  commit work;
  EXCEPTION
    WHEN others THEN
      rollback;
      dbms_output.put_line('Error!');
END;
/

CREATE MATERIALIZED VIEW LOG ON ROBERT.produkty
with PRIMARY KEY
INCLUDING NEW VALUES;

GRANT SELECT ON robert.MLOG$_PRODUKTY TO robert;

commit;