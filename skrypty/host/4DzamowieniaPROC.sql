select * from robert.produkty;
SELECT * FROM ROBERT.ZAMOWIENIA;
CREATE OR REPLACE PROCEDURE robert.anuluj_zamowienie_DOL
(
id_zamowienia_ IN int
)
AS
id_produktu_ int;
ilosc_ int;
CURSOR CUR_DOL IS 
SELECT id_produktu, ilosc from robert.zamowienia_dol where order_id=id_zamowienia_ FOR UPDATE;
BEGIN

  OPEN CUR_DOL;
  FETCH CUR_DOL INTO id_produktu_, ilosc_; 
  IF CUR_DOL%NOTFOUND THEN
    dbms_output.put_line('Error! Order nr '||to_char(id_zamowienia_)||' does not exist!');
    RETURN;
  END IF;
  DELETE FROM robert.zamowienia_dol WHERE CURRENT OF CUR_DOL;
  CLOSE CUR_DOL;
  
  UPDATE robert.produkty
  SET ilosc = ilosc + ilosc_
  WHERE product_id=id_produktu_;
  
  commit work;
  EXCEPTION
    WHEN others THEN
      rollback;
      dbms_output.put_line('Error!');
END;
/

CREATE OR REPLACE PROCEDURE robert.anuluj_zamowienie_NDOL
(
id_zamowienia_ IN int
)
AS
id_produktu_ int;
ilosc_ int;
CURSOR CUR_NDOL IS 
SELECT id_produktu, ilosc from robert.zamowienia_ndol where order_id=id_zamowienia_ FOR UPDATE;
BEGIN

  OPEN CUR_NDOL;
  FETCH CUR_NDOL INTO id_produktu_, ilosc_; 
  IF CUR_NDOL%NOTFOUND THEN
    dbms_output.put_line('Error! Order nr '||to_char(id_zamowienia_)||' does not exist!');
    RETURN;
  END IF;
  DELETE FROM robert.zamowienia_ndol WHERE CURRENT OF CUR_NDOL;
  CLOSE CUR_NDOL;
  
  UPDATE robert.produkty
  SET ilosc = ilosc + ilosc_
  WHERE product_id=id_produktu_;
  
  commit work;
  EXCEPTION
    WHEN others THEN
      rollback;
      dbms_output.put_line('Error!');
END;
/

CREATE OR REPLACE PROCEDURE robert.anuluj_zamowienie
(
id_zamowienia_ IN int,
wojewodztwo_ IN varchar
)
AS
BEGIN

  IF wojewodztwo_='Dolnoœl¹skie' THEN
    robert.anuluj_zamowienie_dol(id_zamowienia_);
  ELSE
    robert.anuluj_zamowienie_ndol(id_zamowienia_);
  END IF;
  
  commit work;
  EXCEPTION
    WHEN others THEN
      rollback;
      dbms_output.put_line('Error!');
END;
/


CREATE OR REPLACE PROCEDURE robert.dodaj_zamowienie
(
id_uzytkownika_ IN int,
id_produktu_ IN int,
ilosc_ IN int,
wojewodztwo_ IN varchar
)
AS
cena float;
wartosc_ float;
  cursor c1 is
    SELECT cena FROM robert.produkty WHERE product_id=id_produktu_ FOR UPDATE;
BEGIN
  
  open c1;
  fetch c1 into cena;
  UPDATE robert.produkty
  SET ilosc = ilosc - ilosc_
  WHERE CURRENT OF c1;
  close c1;
  wartosc_ := cena * ilosc_;
  
  IF wojewodztwo_='Dolnoœl¹skie' THEN
    INSERT INTO robert.zamowienia_dol(order_id, id_uzytkownika, id_produktu, ilosc, wartosc, data_zamowienia, status)
    VALUES (robert.order_seq.NEXTVAL, id_uzytkownika_, id_produktu_, ilosc_, wartosc_, sysdate, 'Przyjête');
  ELSE
    INSERT INTO robert.zamowienia_ndol(order_id, id_uzytkownika, id_produktu, ilosc, wartosc, data_zamowienia, status)
    VALUES (robert.order_seq.NEXTVAL, id_uzytkownika_, id_produktu_, ilosc_, wartosc_, sysdate, 'Przyjête');
  END IF;
  
  commit work;
  EXCEPTION
    WHEN others THEN
      rollback;
      dbms_output.put_line('Error!');
END;
/

CREATE OR REPLACE PROCEDURE robert.zmien_status
(
order_id_ IN int,
status_ IN varchar
)
AS
  status__ varchar(50);
  CURSOR CUR_ZAM IS 
  SELECT status from ROBERT.ZAMOWIENIA_DOL where order_id=order_id_ FOR UPDATE OF status;
  CURSOR CUR_ZAMN IS 
  SELECT status from ROBERT.ZAMOWIENIA_NDOL where order_id=order_id_ FOR UPDATE OF status;
BEGIN
  OPEN CUR_ZAM;
  FETCH CUR_ZAM INTO status__;
  IF CUR_ZAM%NOTFOUND THEN
    CLOSE CUR_ZAM;
    OPEN CUR_ZAMN;
    FETCH CUR_ZAMN INTO status__;
    IF CUR_ZAMN%NOTFOUND THEN
      CLOSE CUR_ZAMN;
      dbms_output.put_line('Error! User does not exist!');
      RETURN;
    END IF;
    
    UPDATE ROBERT.ZAMOWIENIA_NDOL 
    SET status=status_
    WHERE CURRENT OF CUR_ZAMN;
    CLOSE CUR_ZAMN;
    commit;
    RETURN;
  END IF;
  
  UPDATE ROBERT.ZAMOWIENIA_DOL 
  SET status=status_
  WHERE CURRENT OF CUR_ZAM;
  

  CLOSE CUR_ZAM;
  
  commit;
  EXCEPTION
  WHEN others THEN
    dbms_output.put_line( 'Error! ');
    rollback;
END;
/

commit;