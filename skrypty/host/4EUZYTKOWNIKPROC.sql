
CREATE OR REPLACE PROCEDURE robert.insert_user
(login_ IN varchar,
 haslo_ IN varchar,
 imie_ IN varchar,
 nazwisko_ IN varchar,
 wojewodztwo_ IN varchar,
 miasto_ IN varchar,
 kod_pocztowy_ IN varchar,
 ulica_ IN varchar,
 nr_domu_ IN int,
 telefon_ IN number,
 email_ IN varchar
)
AS
idd int;
found int;
BEGIN
  idd := ROBERT.userseq.NEXTVAL;
  SELECT COUNT(*) INTO found FROM robert.uzytkownicy_DOL_data WHERE login=login_;
  IF wojewodztwo_='Dolnoœl¹skie' THEN
    SELECT COUNT(*) INTO found FROM robert.uzytkownicy_NDOL_data WHERE login=login_;
    IF found = 0 THEN
      INSERT INTO ROBERT.uzytkownicy_DOL_data
      VALUES (idd, login_, imie_, nazwisko_, wojewodztwo_, miasto_, kod_pocztowy_, ulica_, nr_domu_, telefon_, email_);
      INSERT INTO ROBERT.uzytkownicy_DOL_pass
      VALUES (idd, login_, haslo_);
      commit;
    ELSE
      dbms_output.put_line( 'Error! User ' || login_ || ' exists! ');
      RETURN;
    END IF;
  ELSE
    SELECT COUNT(*) INTO found FROM robert.uzytkownicy_DOL_data WHERE login=login_;
    IF found = 0 THEN
      INSERT INTO ROBERT.uzytkownicy_NDOL_data
      VALUES (idd, login_, imie_, nazwisko_, wojewodztwo_, miasto_, kod_pocztowy_, ulica_, nr_domu_, telefon_, email_);
      INSERT INTO ROBERT.uzytkownicy_NDOL_pass
      VALUES (idd, login_, haslo_);
      commit;
    ELSE
      dbms_output.put_line( 'Error! User ' || login_ || ' exists! ');
      RETURN;
    END IF;
  END IF;
  EXCEPTION
    WHEN others THEN
      dbms_output.put_line( 'Error! ');
      rollback;
END;
/

commit;


CREATE OR REPLACE PROCEDURE robert.delete_user
(
id_ IN int,
x IN int
)
AS
  order_id_ int;
  wojewodztwo_ varchar(50);
  CURSOR CUR_USER IS 
  SELECT wojewodztwo from robert.uzytkownicy_DOL_data where user_id=id_ FOR UPDATE;
  CURSOR CUR_USERN IS 
  SELECT wojewodztwo from robert.uzytkownicy_NDOL_data where user_id=id_ FOR UPDATE;
BEGIN
  OPEN CUR_USER;
  FETCH CUR_USER INTO wojewodztwo_;
  IF CUR_USER%NOTFOUND THEN
    CLOSE CUR_USER;
    OPEN CUR_USERN;
    FETCH CUR_USERN INTO wojewodztwo_;
    IF CUR_USERN%NOTFOUND THEN
      CLOSE CUR_USERN;
      dbms_output.put_line('Error! User does not exist!');
      RETURN;
    END IF;
    FOR i IN (SELECT order_id FROM robert.zamowienia_NDOL WHERE id_uzytkownika=id_)
    LOOP
      robert.anuluj_zamowienie_NDOL(i.order_id);
    END LOOP;
    DELETE FROM robert.uzytkownicy_NDOL_data WHERE CURRENT OF CUR_USERN;
    CLOSE CUR_USERN;
    commit;
    RETURN;
  END IF;
  
  FOR i IN (SELECT order_id FROM robert.zamowienia_DOL WHERE id_uzytkownika=id_)
  LOOP
      robert.anuluj_zamowienie_DOL(i.order_id);
  END LOOP;
  
  DELETE FROM robert.uzytkownicy_DOL_data WHERE CURRENT OF CUR_USER;

  CLOSE CUR_USER;
  
  commit;
  EXCEPTION
  WHEN others THEN
    dbms_output.put_line( 'Error! ');
    rollback;
END;
/
COMMIT;