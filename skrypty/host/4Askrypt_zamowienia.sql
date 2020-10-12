--drop table robert.zamowienia_dol;
create table robert.zamowienia_dol(
order_id int NOT NULL,
id_uzytkownika int NOT NULL,
id_produktu int NOT NULL,
ilosc int NOT NULL,
wartosc number(9,2) NOT NULL,
status varchar(50),
data_zamowienia date NOT NULL,
PRIMARY KEY (order_id),
FOREIGN KEY (id_uzytkownika) REFERENCES robert.uzytkownicydol_pass(user_id),
FOREIGN KEY (id_produktu) REFERENCES robert.produkty(product_id)
);

ALTER TABLE robert.zamowienia_dol
ADD CHECK (ilosc>=0 and wartosc>=0);

CREATE INDEX robert.index_zamowienia_dol_usr
ON robert.zamowienia_dol(id_uzytkownika);

CREATE INDEX robert.index_zamowienia_dol_prod
ON robert.zamowienia_dol(id_produktu);

CREATE SEQUENCE robert.order_seq
MINVALUE 0
START WITH 1
INCREMENT BY 1
CACHE 10;


commit;