Cel projektu 
==========

Stworzenie systemu zakupów internetowych przy użyciu rozproszonych baz danych.

Wymagania
==========

System zarządzania bazą danych: Oracle 11g

Technologia użyta do stworzenia aplikacji webowej: Python 3.7 + Django

Funkcjonalności:
==============
1. Możliwość założenia konta użytkownika

2. Dostęp do konta administratora oraz kont klientów(użytkowników)

3. Administrator ma możliwość:
* przeglądania i filtrowania użytkowników, pracowników, produktów oraz złożonych zamówień;
* edytowania informacji o pracownikach, produktach i użytkownikach;
* dodawania produktów i pracowników;
* usuwania pracowników, użytkowników oraz zamówień;
* zmieniania statusu(przyjęte, realizowane lub wykonane) zamówień

4. Użytkownik ma możliwość:
* przeglądania produktów;
* składania zamówień;
* anulowania zamówień

Konfiguracja projektu
===================

I. Konfiguracja baz danych

1. Stwórz maszynę wirtualną w programie VirtualBox
2. Zainstaluj na maszynach(maszyna wirtualna + host) system zarządzania bazą danych Oracle 11g
3. Na maszynach hosta oraz wirtualnej utwórz odpowiednio bazy danych ORCL i ORCL1
4. Skonfiguruj połączenie pomiędzy hostem, a maszyną wirtualną
5. Uruchom wszystkie skrypty sql w folderze skrypty/host na maszynie hosta
6. Uruchom wszystkie skrypty sql w folderze skrypty/vm na maszynie wirtualnej
7. Na maszynie hosta połącz się z systemem bazy danych jako użytkownik stradmin
8. Uruchom skrypty skrypty/hostStrm/8Adblink.sql oraz skrypty/hostStrm/8BprocesyRepl.sql
9. Na maszynie wirtualnej połącz się z systemem bazy danych jako użytkownik stradmin
10. Uruchom skrypty skrypty/hostStrm/8Adblink.sql oraz skrypty/hostStrm/8BProcesyRpldbvmStr.sql

II. Uruchomienie aplikacji

Wymagania: Python 3.7, Django, cx_Oracle.
1. Uruchom commander i przejdź do folderu appka/ zawierającego skrypt manage.py
2. Uruchom polecenie: python manage.py runserver
3. Uruchom przeglądarkę i wejdź na stronę http://127.0.0.1:8000/sklep/login


TODO:
====

* refaktoryzacja kodu
* dokumentacja