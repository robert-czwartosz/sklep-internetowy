BEGIN
DBMS_STREAMS_ADM.SET_UP_QUEUE( 
  queue_name => 'capture_queue', 
  queue_user => 'STRADMIN'); 
 
DBMS_STREAMS_ADM.SET_UP_QUEUE( 
  queue_name=>'apply_queue', 
  queue_user=>'STRADMIN'); 
END;
/

--select * from  USER_QUEUES;
--EXECUTE  DBMS_AQADM.STOP_QUEUE(queue_name => 'capture_queue');
--EXECUTE  DBMS_AQADM.DROP_QUEUE(queue_name => 'capture_queue');
/*--EXEC dbms_streams_adm.remove_queue('stradmin.capture_queue',FALSE,TRUE);*/

--EXECUTE  DBMS_AQADM.STOP_QUEUE(queue_name => 'apply_queue');
--EXECUTE  DBMS_AQADM.DROP_QUEUE(queue_name => 'apply_queue');

--EXECUTE  DBMS_AQADM.DROP_QUEUE_TABLE(queue_table => 'STREAMS_QUEUE_TABLE');
--drop sequence "STRADMIN"."AQ$_STREAMS_QUEUE_TABLE_N";