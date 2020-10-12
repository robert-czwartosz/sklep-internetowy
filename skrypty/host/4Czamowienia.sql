CREATE VIEW robert.zamowienia
AS 
SELECT * from robert.zamowienia_dol
UNION
SELECT * from robert.zamowienia_ndol;

select * from robert.zamowienia;
select * from robert.zamowienia_DOL;
select * from robert.zamowienia_NDOL;