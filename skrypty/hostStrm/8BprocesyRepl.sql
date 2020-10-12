DECLARE
	cscn NUMBER;
BEGIN
-- zdefiniowanie kolejek
DBMS_STREAMS_ADM.SET_UP_QUEUE( 
  queue_name => 'capture_queue', 
  queue_user => 'STRADMIN'); 
 
DBMS_STREAMS_ADM.SET_UP_QUEUE( 
  queue_name=>'apply_queue', 
  queue_user=>'STRADMIN'); 
  
--zdefiniowanie procesów CAPTURE 
 
DBMS_STREAMS_ADM.ADD_TABLE_RULES( 
  table_name      =>'robert.pracownicy', 
  streams_type    =>'sync_capture',  
  streams_name    =>'sync_capture', 
  queue_name      =>'stradmin.capture_queue'); 

--propagacja zmian z PN do PD 

DBMS_STREAMS_ADM.ADD_TABLE_PROPAGATION_RULES( 
  table_name              =>'robert.pracownicy', 
  streams_name            =>'send_robert_pracownicy', 
  source_queue_name       =>'stradmin.capture_queue', 
  destination_queue_name  =>'stradmin.apply_queue@ORCL1', 
  source_database         =>'ORCL', 
  queue_to_queue          =>TRUE); 
 
--definicja procesów APPLY 
 
DBMS_APPLY_ADM.CREATE_APPLY( 
  queue_name      =>'stradmin.apply_queue', 
  apply_name      =>'apply_robert_pracownicy', 
  apply_captured  => FALSE); 
   
--wprowadzanie zmian z kolejki APPLY 
 
DBMS_STREAMS_ADM.ADD_TABLE_RULES( 
  table_name      =>'robert.pracownicy', 
  streams_type    =>'apply', 
  streams_name    =>'apply_robert_pracownicy', 
  queue_name      =>'stradmin.apply_queue', 
  source_database =>'ORCL1'); 
  
cscn := DBMS_FLASHBACK.GET_SYSTEM_CHANGE_NUMBER();
DBMS_APPLY_ADM.SET_TABLE_INSTANTIATION_SCN@ORCL1(
	source_object_name		=> 'robert.pracownicy',
	source_database_name	=> 'ORCL',
	instantiation_scn		=> cscn);

--uruchomienie procesu apply  
DBMS_APPLY_ADM.START_APPLY( 
  apply_name  =>'apply_robert_pracownicy'); 
END;
/