--CREATE PUBLIC DATABASE LINK orcl CONNECT TO robert identified by qwerty using '192.168.56.1/orcl';
--CREATE PUBLIC DATABASE LINK orcl1 CONNECT TO robert identified by qwerty using '192.168.56.11/orcl1';



CREATE MATERIALIZED VIEW robert.produkty
  BUILD IMMEDIATE 
  REFRESH FAST
  NEXT sysdate+(1/(24*60*6))
  WITH PRIMARY KEY
AS 
SELECT * FROM robert.produkty@orcl;

--GRANT ON COMMIT REFRESH TO "SYSTEM";
select * from robert.produkty@orcl;
select * from robert.produkty@ORCL1;
