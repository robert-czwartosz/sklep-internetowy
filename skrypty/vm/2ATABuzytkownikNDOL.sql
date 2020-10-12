/*CREATE TABLESPACE TB_SPACE_HOST DATAFILE '\\VBoxSvr\orcl\TBSPACE_HOST.DBF' SIZE 55M
EXTENT MANAGEMENT LOCAL AUTOALLOCATE;

ALTER USER "SYS" QUOTA UNLIMITED ON TB_SPACE_HOST;
GRANT UNLIMITED TABLESPACE TO "SYS" WITH ADMIN OPTION;
GRANT dba TO "SYS";
select * from dba_sys_privs where grantee='SYS';
*/
create table robert.uzytkownicyNDOL_data(
user_id int NOT NULL,
login varchar(50) NOT NULL UNIQUE,
imie varchar(50) NOT NULL,
nazwisko varchar(50) NOT NULL,
wojewodztwo varchar(50) NOT NULL,
miasto varchar(50) NOT NULL,
kod_pocztowy varchar(50) NOT NULL,
ulica varchar(50) NOT NULL,
nr_domu varchar(10) NOT NULL,
telefon number(12) NOT NULL,
email varchar(50) NOT NULL,
PRIMARY KEY (user_id)
);

ALTER TABLE robert.uzytkownicyNDOL_data
ADD CHECK (length(login)>=8);

create table robert.uzytkownicyNDOL_pass(
user_id int NOT NULL UNIQUE,
login varchar(50) NOT NULL UNIQUE,
haslo varchar(50) NOT NULL
);

ALTER TABLE robert.uzytkownicyNDOL_pass
ADD CONSTRAINT fk_user FOREIGN KEY (user_id) 
REFERENCES robert.uzytkownicyNDOL_data(user_id) 
ON DELETE CASCADE;

ALTER TABLE robert.uzytkownicyNDOL_pass
ADD CHECK (length(login)>=8 and length(haslo)>=8);