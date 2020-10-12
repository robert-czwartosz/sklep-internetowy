CREATE SYNONYM ROBERT.UZYTKOWNICY_DOL_PASS
FOR robert.UZYTKOWNICYDOL_PASS@ORCL;
CREATE SYNONYM ROBERT.UZYTKOWNICY_DOL_DATA
FOR robert.UZYTKOWNICYDOL_DATA@ORCL;

CREATE SYNONYM ROBERT.UZYTKOWNICY_NDOL_PASS
FOR robert.UZYTKOWNICYNDOL_PASS;
CREATE SYNONYM ROBERT.UZYTKOWNICY_NDOL_DATA
FOR robert.UZYTKOWNICYNDOL_DATA;

CREATE SYNONYM ROBERT.userseq
FOR robert.user_seq@orcl;

CREATE VIEW robert.uzytkownicy
AS 
SELECT UZYTKOWNICY_DOL_PASS.HASLO, UZYTKOWNICY_DOL_DATA.* FROM UZYTKOWNICY_DOL_PASS FULL JOIN UZYTKOWNICY_DOL_DATA ON UZYTKOWNICY_DOL_DATA.login = UZYTKOWNICY_DOL_PASS.login
UNION
SELECT UZYTKOWNICY_NDOL_PASS.HASLO, UZYTKOWNICY_NDOL_DATA.*  FROM UZYTKOWNICY_NDOL_PASS FULL JOIN UZYTKOWNICY_NDOL_DATA ON UZYTKOWNICY_NDOL_DATA.login = UZYTKOWNICY_NDOL_PASS.login;

select * from robert.uzytkownicy;
select * from robert.uzytkownicy_DOL_DATA;