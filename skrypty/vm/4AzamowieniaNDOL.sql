--drop table robert.zamowienia_ndol;
create table robert.zamowienia_ndol(
order_id int NOT NULL,
id_uzytkownika int NOT NULL,
id_produktu int NOT NULL,
ilosc int NOT NULL,
wartosc number(9,2) NOT NULL,
status varchar(50),
data_zamowienia date NOT NULL,
PRIMARY KEY (order_id),
FOREIGN KEY (id_uzytkownika) REFERENCES robert.uzytkownicyNDOL_pass(user_id),
FOREIGN KEY (id_produktu) REFERENCES robert.produkty(product_id)
);
 

ALTER TABLE robert.zamowienia_ndol
ADD CHECK (ilosc>=0 and wartosc>=0);

CREATE INDEX robert.index_zamowienia_ndol_usr
ON robert.zamowienia_ndol(id_uzytkownika);

CREATE INDEX robert.index_zamowienia_ndol_prod
ON robert.zamowienia_ndol(id_produktu);
