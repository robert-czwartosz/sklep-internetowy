select name from v$database;
select * from robert.produkty where ilosc like '%2%';
select * from robert.produkty where ilosc<24;
select * from robert.produkty@ORCL1;
select * from robert.zamowienia;
select * from robert.zamowienia_dol;-- where data_zamowienia like '%19/12/28%';
select * from robert.zamowienia_ndol;
select * from robert.uzytkownicy;
select * from robert.uzytkownicy_DOL_pass;
select * from robert.uzytkownicy_DOL_data where wojewodztwo like '%Dolnoœl¹skie%' and telefon like '%%';
select * from robert.uzytkownicy_NDOL_data;
select * from robert.uzytkownicy_NDOL_pass;
--select * from robert.uzytkownicy PARTITION (dol);
--select * from robert.uzytkownicy PARTITION (pozostale);
select * from robert.pracownicy@orcl;
select * from robert.pracownicy@orcl1;
execute robert.dodaj_pracownika('Jan','Cz.',342456982, 'Stanowisko',3000);
execute robert.usun_pracownika(2);
select index_name, table_name from all_indexes where table_name='UZYTKOWNICY';

SELECT order_id FROM robert.zamowienia_DOL WHERE id_uzytkownika=2;

execute robert.delete_user(2,0);
execute robert.insert_product('produkt 4', 20, 120.2149, 'to jest produkt nr 10');
execute ROBERT.INSERT_USER('loginxusera3', 'haslousera', 'Robert', 'Cz.', 'Dolnoœl¹skie', 'Trzebnica', '33-321', 'ulica', 21, 111222333, 'robert@robert.pl');
execute ROBERT.INSERT_USER('loginxusera1', 'haslousera', 'Robert', 'Cz.', 'Wielkopolskie', 'Trzebnica', '33-321', 'ulica', 21, 111222333, 'robert@robert.pl');
execute ROBERT.DODAJ_ZAMOWIENIE(4, 2, 10, 'Dolnoœl¹skie');
EXECUTE ROBERT.DOSTAWA_PRODUKTU('produkt 3', 10);
execute ROBERT.ANULUJ_ZAMOWIENIE(3, 'Dolnoœl¹skie');

SELECT TO_DATE('19/12/06') from dual;
commit;