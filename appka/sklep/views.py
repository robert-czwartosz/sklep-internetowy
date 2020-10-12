from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404


from .forms import *

import cx_Oracle


from importlib import import_module
from django.conf import settings

from datetime import datetime
import time

TEMPLATE_PATHH = 'C:\\Users\\User\\Desktop\\appka\\sklep\\templates\\sklep\\'

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			login = form.cleaned_data['login']
			haslo = form.cleaned_data['haslo']
			imie = form.cleaned_data['imie']
			nazwisko = form.cleaned_data['nazwisko']
			miasto = form.cleaned_data['miasto']
			wojewodztwo = form.cleaned_data['wojewodztwo']
			kod_pocztowy = form.cleaned_data['kod_pocztowy']
			ulica = form.cleaned_data['ulica']
			nr_domu = form.cleaned_data['nr_domu']
			telefon = form.cleaned_data['telefon']
			email = form.cleaned_data['email']
			
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			print(con.version)
			cur = con.cursor()
			cur.callproc('insert_user', (login, haslo, imie,nazwisko,wojewodztwo,miasto,kod_pocztowy,ulica,nr_domu,telefon,email))
			cur.close()
			con.close()
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

def login(request):
	print(request.session.get_session_cookie_age())
	if 'loggedin' in request.session:
		if request.session['loggedin']:
			return HttpResponseRedirect(reverse('sklep:loggedin'))
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			login = form.cleaned_data['login']
			haslo = form.cleaned_data['haslo']
			request.session['_login_'] = login
			request.session['_haslo_'] = haslo
			request.session.modified = True
			return HttpResponseRedirect(reverse('sklep:auth'))
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form})

def auth(request):
	if '_login_' in request.session and '_haslo_' in request.session:
		login = request.session['_login_']
		haslo = request.session['_haslo_']
	else:
		return HttpResponseRedirect(reverse('sklep:login'))

	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	print(con.version)
	cur = con.cursor()
	cur.prepare('select user_id, wojewodztwo from uzytkownicy where login=:login and haslo=:haslo')
	cur.execute(None,{'login': login, 'haslo': haslo})
	user = cur.fetchall()
	cur.close()
	con.close()
	print(user)
	if(len(user) > 0):
		print(user)
		request.session.set_expiry(900)
		request.session['_id'] = user[0][0]
		request.session['_wojewodztwo_'] = user[0][1]
		request.session['loggedin'] = True
		request.session['admin'] = False
		if login=='Administrator':
			request.session['admin'] = True
		request.session.modified = True
		return HttpResponseRedirect(reverse('sklep:loggedin'))
	return HttpResponseRedirect(reverse('sklep:login'))

def loggedin(request):
	if 'loggedin' in request.session:
		if request.session['loggedin']:
			user_id = request.session['_id']
			login = request.session['_login_']
			request.session.modified = True
			admin = request.session['admin']
			print(request.session['admin'])
			print(request.session['_login_'])
			if admin:
				return HttpResponseRedirect(reverse('sklep:listprod'))
			else:
				return HttpResponseRedirect(reverse('sklep:listprodUser', args=(user_id,)))
			return render(request, 'loggedin.html', {'login': [login], 'admin': admin, 'user':login})
	return HttpResponseRedirect(reverse('sklep:login'))

def loggedout(request):
	request.session.clear()
	request.session.flush()
	#return render(request, 'loggedout.html', {})
	return HttpResponseRedirect(reverse('sklep:login'))

def addProduct(request):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			nazwa = form.cleaned_data['nazwa']
			ilosc = form.cleaned_data['ilosc']
			cena = form.cleaned_data['cena']
			opis = form.cleaned_data['opis']
			
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			print(con.version)
			cur = con.cursor()
			cur.callproc('insert_product', (nazwa, ilosc, cena, opis))
			cur.close()
			con.close()
			return HttpResponseRedirect(reverse('sklep:listprod'))
	else:
		form = ProductForm()
	return render(request, 'addproduct.html', {'admin': admin, 'form': form})

def listProd(request):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	print(con.version)
	cur = con.cursor()
	cur.execute('select * from produkty order by product_id')
	results = cur.fetchall()
	context = {'results': results, 'admin':admin, 'edit': False }
	cur.close()
	con.close()
	return render(request, TEMPLATE_PATHH+'listProd.html', context)
"""
def deleteProd(request,prod_id =None):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	cur = con.cursor()
	cur.prepare('delete from produkty where product_id=:id')
	cur.execute(None, {'id':prod_id})
	cur.close()
	con.commit()
	con.close()
	return HttpResponseRedirect(reverse('sklep:listprod'))
"""
def editProd(request, prod_id):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	print(con.version)
	cur = con.cursor()
	cur.execute('select * from produkty order by product_id')
	results = cur.fetchall()
	cur.close()
	con.close()
	if request.method == "POST":
		form = ProductForm(request.POST)
		if form.is_valid():
			nazwa = form.cleaned_data['nazwa']
			ilosc = form.cleaned_data['ilosc']
			cena = form.cleaned_data['cena']
			opis = form.cleaned_data['opis']
			def toString(obj):
				if obj==None:
					return ''
				else:
					return obj
			prod = [prod_id, nazwa, ilosc, cena, opis]
			prod = [toString(u) for u in prod]
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			cur = con.cursor()

			cur.prepare('UPDATE produkty SET nazwa = :nazwa , ilosc = :ilosc , cena = :cena , opis = :opis WHERE product_id=:id')
			cur.execute(None, {'id':prod[0],
								'nazwa': prod[1],
							   'ilosc': prod[2],
							   'cena': prod[3],
							   'opis': prod[4]})
			con.commit()
			cur.close()
			con.close()
			return HttpResponseRedirect(reverse('sklep:listprod'))
	else:
		form = ProductForm()
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
	return render(request, 'listProd.html', {'admin': admin, 'results': results, 'edit': True, 'form': form})


def addEmp(request):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	if request.method == 'POST':
		form = EmpForm(request.POST)
		if form.is_valid():
			imie = form.cleaned_data['imie']
			nazwisko = form.cleaned_data['nazwisko']
			pesel = form.cleaned_data['pesel']
			stanowisko = form.cleaned_data['stanowisko']
			wynagrodzenie = form.cleaned_data['wynagrodzenie']
			
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			print(con.version)
			cur = con.cursor()
			cur.callproc('dodaj_pracownika', (imie, nazwisko, pesel, stanowisko, wynagrodzenie))
			cur.close()
			con.close()
			return HttpResponseRedirect(reverse('sklep:listemp'))
	else:
		form = EmpForm()
	return render(request, 'addemp.html', {'form': form, 'admin': admin})

def listEmp(request):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	print(con.version)
	cur = con.cursor()
	cur.execute('select * from pracownicy order by emp_id')
	results = cur.fetchall()
	context = {'form': EmpForm(), 'edit': False, 'results': results, 'admin': admin}
	cur.close()
	con.close()
	return render(request, TEMPLATE_PATHH+'listEmp.html', context)

def deleteEmp(request,emp_id =None):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	cur = con.cursor()
	cur.prepare('delete from pracownicy where emp_id=:id')
	cur.execute(None, {'id':emp_id})
	cur.close()
	con.commit()
	con.close()
	return HttpResponseRedirect(reverse('sklep:listemp'))

def editEmp(request, emp_id):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	print(con.version)
	cur = con.cursor()
	cur.execute('select * from pracownicy order by emp_id')
	results = cur.fetchall()
	cur.close()
	con.close()
	if request.method == "POST":
		form = EmpForm(request.POST)
		if form.is_valid():
			imie = form.cleaned_data['imie']
			nazwisko = form.cleaned_data['nazwisko']
			pesel = form.cleaned_data['pesel']
			stanowisko = form.cleaned_data['stanowisko']
			wynagrodzenie = form.cleaned_data['wynagrodzenie']
			def toString(obj):
				if obj==None:
					return ''
				else:
					return obj
			emp = [emp_id, imie, nazwisko, pesel, stanowisko, wynagrodzenie]
			emp = [toString(u) for u in emp]
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			cur = con.cursor()

			cur.prepare('UPDATE pracownicy SET imie = :imie , nazwisko = :nazwisko , pesel = :pesel , stanowisko = :stanowisko , wynagrodzenie = :wynagrodzenie WHERE emp_id=:id')
			cur.execute(None, {'id':emp[0],
								'imie': emp[1],
							   'nazwisko': emp[2],
							   'pesel': emp[3],
							   'stanowisko': emp[4],
							   'wynagrodzenie':emp[5]})
			con.commit()
			cur.close()
			con.close()
			return HttpResponseRedirect(reverse('sklep:listemp'))
	else:
		form = EmpForm()
	return render(request, 'listEmp.html', {'form': form, 'results': results, 'admin': admin, 'edit': True})

def findUser(request):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			login = form.cleaned_data['login']
			imie = form.cleaned_data['imie']
			nazwisko = form.cleaned_data['nazwisko']
			wojewodztwo = form.cleaned_data['wojewodztwo']
			miasto = form.cleaned_data['miasto']
			kod_pocztowy = form.cleaned_data['kod_pocztowy']
			ulica = form.cleaned_data['ulica']
			nr_domu = form.cleaned_data['nr_domu']
			telefon = form.cleaned_data['telefon']
			if telefon==None:
				telefon = ''
			email = form.cleaned_data['email']
			def toString(obj):
				if obj==None:
					return '%'
				if type(obj) is int or type(obj) is float:
					return str(obj)
				else:
					return '%'+str(obj)+'%'
			user = [login, imie, nazwisko, wojewodztwo, miasto, kod_pocztowy,
					ulica, nr_domu, telefon, email]
			user = [toString(u) for u in user]
			request.session['user'] = user
			print(user)
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			print(con.version)
			cur = con.cursor()
			cur.prepare('select user_id, login, imie, nazwisko, wojewodztwo, miasto, kod_pocztowy, ulica, nr_domu, telefon, email from uzytkownicy where login like :login and imie like :imie and nazwisko like :nazwisko and miasto like :miasto and wojewodztwo like :wojewodztwo and kod_pocztowy like :kod_pocztowy and ulica like :ulica and nr_domu like :nr_domu and telefon like :telefon and email like :email')
			cur.execute(None, {'login':user[0],
							   'imie': user[1],
							   'nazwisko': user[2],
							   'wojewodztwo': user[3],
							   'miasto': user[4],
							   'kod_pocztowy':user[5],
							   'ulica': user[6],
							   'nr_domu': user[7],
							   'telefon': user[8],
							   'email': user[9]})
			results = cur.fetchall()
			print(results)
			context = {'admin': admin, 'title': ['Wyszukiwanie uzytkownika'], 'form': UserForm(), 'results': results, 'edit': False}
			cur.close()
			con.close()
			return render(request, TEMPLATE_PATHH+'findusr.html', context)
	if 'user' in request.session:
		user = request.session['user']
		request.session['user'] = user
		form = UserForm()
		print(user)
		con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
						cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
		cur = con.cursor()
		cur.prepare('select user_id, login, imie, nazwisko, wojewodztwo, miasto, kod_pocztowy, ulica, nr_domu, telefon, email from uzytkownicy where login like :login and imie like :imie and nazwisko like :nazwisko and miasto like :miasto and wojewodztwo like :wojewodztwo and kod_pocztowy like :kod_pocztowy and ulica like :ulica and nr_domu like :nr_domu and telefon like :telefon and email like :email')
		cur.execute(None, {'login':user[0],
							'imie': user[1],
						   'nazwisko': user[2],
						   'wojewodztwo': user[3],
						   'miasto': user[4],
						   'kod_pocztowy':user[5],
						   'ulica': user[6],
						   'nr_domu': user[7],
						   'telefon': user[8],
							'email': user[9]})
		results = cur.fetchall()
		print(results)
		context = {'form': form, 'results': results, 'admin': admin}
		cur.close()
		con.close()
		return render(request, TEMPLATE_PATHH+'findusr.html', context)
	form = UserForm()
	return render(request, 'findusr.html', {'title': ['Wyszukiwanie uzytkownika'], 'admin': admin, 'form': form, 'results': [], 'edit': False})

def deleteUser(request,user_id =None):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	cur = con.cursor()
	cur.callproc('delete_user', (user_id, 0))
	cur.close()
	con.commit()
	con.close()
	return HttpResponseRedirect(reverse('sklep:findusr'))

def editUser(request, user_id):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	results = []
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			imie = form.cleaned_data['imie']
			nazwisko = form.cleaned_data['nazwisko']
			miasto = form.cleaned_data['miasto']
			kod_pocztowy = form.cleaned_data['kod_pocztowy']
			ulica = form.cleaned_data['ulica']
			nr_domu = form.cleaned_data['nr_domu']
			telefon = form.cleaned_data['telefon']
			email = form.cleaned_data['email']
			def toString(obj):
				if obj==None:
					return ''
				else:
					return obj
			user = [user_id, imie, nazwisko, miasto, kod_pocztowy,
					ulica, nr_domu, telefon, email]
			user = [toString(u) for u in user]
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			cur = con.cursor()
			cur.prepare('UPDATE uzytkownicy SET imie = :imie , nazwisko = :nazwisko , miasto = :miasto , kod_pocztowy = :kod_pocztowy , ulica = :ulica , nr_domu = :nr_domu , telefon = :telefon , email = :email WHERE user_id=:id')
			cur.execute(None, {'id':user[0],
								'imie': user[1],
							   'nazwisko': user[2],
							   'miasto': user[3],
							   'kod_pocztowy':user[4],
							   'ulica': user[5],
							   'nr_domu': user[6],
							   'telefon': user[7],
								'email': user[8]})
			con.commit()

			cur.close()
			con.close()
			return HttpResponseRedirect(reverse('sklep:findusr'))
	else:
		if 'user' in request.session:
			user = request.session['user']
			request.session['user'] = user
			form = UserForm()
			print(user)
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			cur = con.cursor()
			cur.prepare('select user_id, login, imie, nazwisko, wojewodztwo, miasto, kod_pocztowy, ulica, nr_domu, telefon, email from uzytkownicy where login like :login and imie like :imie and nazwisko like :nazwisko and miasto like :miasto and wojewodztwo like :wojewodztwo and kod_pocztowy like :kod_pocztowy and ulica like :ulica and nr_domu like :nr_domu and telefon like :telefon and email like :email')
			cur.execute(None, {'login':user[0],
								'imie': user[1],
							   'nazwisko': user[2],
							   'wojewodztwo': user[3],
							   'miasto': user[4],
							   'kod_pocztowy':user[5],
							   'ulica': user[6],
							   'nr_domu': user[7],
							   'telefon': user[8],
								'email': user[9]})
			results = cur.fetchall()
			cur.close()
			con.close()
		form = UserForm()
		form.fields['login'].widget = forms.HiddenInput()
		form.fields['wojewodztwo'].widget = forms.HiddenInput()
	return render(request, 'findusr.html', {'title': ['Edycja uzytkownika'], 'admin': admin,'form': form, 'results': results, 'edit': True})

def findOrder(request):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	results = []
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			status = form.cleaned_data['status']
			id_uzytkownika = form.cleaned_data['id_uzytkownika']
			id_produktu = form.cleaned_data['id_produktu']
			ilosc_min = form.cleaned_data['ilosc_min']
			ilosc_max = form.cleaned_data['ilosc_max']
			wartosc_min = form.cleaned_data['wartosc_min']
			wartosc_max = form.cleaned_data['wartosc_max']
			data_zamowienia_od = form.cleaned_data['data_zamowienia_od']
			data_zamowienia_do = form.cleaned_data['data_zamowienia_do']
			order = [status, id_uzytkownika, id_produktu, ilosc_min, ilosc_max,
					 wartosc_min, wartosc_max, data_zamowienia_od, data_zamowienia_do]
			print(order)
			def toString(obj):
				if obj==None:
					return '%'
				if type(obj) is int or type(obj) is float:
					return obj
				if type(obj) is str:
					return '%'+obj+'%'
				else:
					return obj
			order = [toString(o) for o in order]
			order_sess = list(order)
			if data_zamowienia_od!=None:
				order_sess[-2] = data_zamowienia_od.strftime('%Y %m %d')
			else:
				order[-2] = datetime.strptime("2000 1 1", '%Y %m %d')
				order_sess[-2] = "2000 1 1"
			if data_zamowienia_do!=None:
				order_sess[-1] = data_zamowienia_do.strftime('%Y %m %d')
			else:
				order[-1] = datetime.strptime("2100 12 31", '%Y %m %d')
				order_sess[-1] = "2100 12 31"
			print("POST")
			print(order)
			print(order_sess)
			request.session['order'] = order_sess
			
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			print(con.version)
			cur = con.cursor()
			cur.prepare('select order_id, id_uzytkownika, id_produktu, ilosc, wartosc, status, data_zamowienia from zamowienia where id_uzytkownika like :id_uzytkownika and id_produktu like :id_produktu and ilosc > :ilosc_min and ilosc < :ilosc_max and wartosc > :wartosc_min and wartosc < :wartosc_max and data_zamowienia >= :data_zamowienia_od and data_zamowienia <= :data_zamowienia_do and status like :status')
			cur.execute(None, {'status': order[0],
							'id_uzytkownika':order[1],
							'id_produktu': order[2],
						   'ilosc_min': order[3],
						   'ilosc_max': order[4],
						   'wartosc_min': order[5],
						   'wartosc_max':order[6],
						   'data_zamowienia_od': order[7],
						   'data_zamowienia_do': order[8]})
			results = cur.fetchall()
			for i in range(len(results)):
				results[i] = list(results[i])
				results[i][-1] = results[i][-1].strftime('%d-%m-%Y %H:%M')
			print(results)
			context = {'results': results}
			cur.close()
			con.close()
			return render(request, 'findord.html', {'form': form, 'results': results, 'admin': admin})
	form = OrderForm()
	if 'order' in request.session:
		order = request.session['order']
		request.session['order'] = order
		order = list(order)
		order[-1] = datetime.strptime(order[-1], "%Y %m %d")
		order[-2] = datetime.strptime(order[-2], "%Y %m %d")
		form = OrderForm()
		print(order)
		con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
						cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
		cur = con.cursor()
		cur.prepare('select order_id, id_uzytkownika, id_produktu, ilosc, wartosc, status, data_zamowienia from zamowienia where id_uzytkownika like :id_uzytkownika and id_produktu like :id_produktu and ilosc > :ilosc_min and ilosc < :ilosc_max and wartosc > :wartosc_min and wartosc < :wartosc_max and data_zamowienia >= :data_zamowienia_od and data_zamowienia <= :data_zamowienia_do and status like :status')
		cur.execute(None, {'status': order[0],
							'id_uzytkownika':order[1],
							'id_produktu': order[2],
						   'ilosc_min': order[3],
						   'ilosc_max': order[4],
						   'wartosc_min': order[5],
						   'wartosc_max':order[6],
						   'data_zamowienia_od': order[7],
						   'data_zamowienia_do': order[8]})
		results = cur.fetchall()
		for i in range(len(results)):
			results[i] = list(results[i])
			results[i][-1] = results[i][-1].strftime('%d-%m-%Y %H:%M')
		print(results)
		context = {'form': form, 'results': results}
		cur.close()
		con.close()
		#return render(request, TEMPLATE_PATHH+'findord.html', context)
	return render(request, 'findord.html', {'form': form, 'results': results, 'admin': admin})

def deleteOrder(request, order_id=None, user_id=None):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	cur = con.cursor()
	cur.prepare('select login from uzytkownicy where user_id=:id')
	cur.execute(None, {'id':user_id})
	result = cur.fetchall()
	wojewodztwo = 'NieDolnośląskie'
	if len(result) > 0:
		wojewodztwo = 'Dolnośląskie'
	print(result)
	cur.callproc('anuluj_zamowienie', (order_id, wojewodztwo))
	cur.close()
	con.commit()
	con.close()
	return HttpResponseRedirect(reverse('sklep:findord'))

def orderSetStatus(request, order_id=None):
	request.session.modified = True
	admin = False
	if 'admin' in request.session:
		admin = request.session['admin']
		if admin == False:
			return HttpResponseRedirect(reverse('sklep:login'))
	else:
		return HttpResponseRedirect(reverse('sklep:login'))
	print(request.POST)
	if request.method == 'POST':
		if 'status' in request.POST:
			status = request.POST['status']
			print(status)
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
									cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			print(con.version)
			cur = con.cursor()
			cur.callproc('zmien_status', (order_id, status))
			cur.close()
			con.close() 
	return HttpResponseRedirect(reverse('sklep:findord'))

##########################################################################
############################# USER ####################################
#############################################################

def findOrderUser(request, user_id=None):
	request.session.modified = True
	request.session.set_expiry(900)
	if '_login_' not in request.session or request.session.get('_id', None)!=user_id:
		return HttpResponseRedirect(reverse('sklep:login'))
	user = request.session['_login_']
	results = []
	if request.method == 'POST':
		form = OrderForm(request.POST)
		form.fields['id_uzytkownika'].widget = forms.HiddenInput()
		if form.is_valid():
			id_uzytkownika = user_id
			status = form.cleaned_data['status']
			id_produktu = form.cleaned_data['id_produktu']
			ilosc_min = form.cleaned_data['ilosc_min']
			ilosc_max = form.cleaned_data['ilosc_max']
			wartosc_min = form.cleaned_data['wartosc_min']
			wartosc_max = form.cleaned_data['wartosc_max']
			data_zamowienia_od = form.cleaned_data['data_zamowienia_od']
			data_zamowienia_do = form.cleaned_data['data_zamowienia_do']
			order = [status, id_uzytkownika, id_produktu, ilosc_min, ilosc_max,
					 wartosc_min, wartosc_max, data_zamowienia_od, data_zamowienia_do]
			print(order)
			def toString(obj):
				if obj==None:
					return '%'
				if type(obj) is int or type(obj) is float:
					return obj
				if type(obj) is str:
					return '%'+obj+'%'
				else:
					return obj
			order = [toString(o) for o in order]
			order_sess = list(order)
			if data_zamowienia_od!=None:
				order_sess[-2] = data_zamowienia_od.strftime('%Y %m %d')
			else:
				order[-2] = datetime.strptime("2000 1 1", '%Y %m %d')
				order_sess[-2] = "2000 1 1"
			if data_zamowienia_do!=None:
				order_sess[-1] = data_zamowienia_do.strftime('%Y %m %d')
			else:
				order[-1] = datetime.strptime("2100 12 31", '%Y %m %d')
				order_sess[-1] = "2100 12 31"
			print("POST")
			print(order)
			print(order_sess)
			request.session['order'] = order_sess
			
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			print(con.version)
			cur = con.cursor()
			if request.session['_wojewodztwo_']=='Dolnośląskie':
				cur.prepare('select order_id, id_uzytkownika, id_produktu, ilosc, wartosc, status, data_zamowienia from zamowienia_DOL where id_uzytkownika like :id_uzytkownika and id_produktu like :id_produktu and ilosc > :ilosc_min and ilosc < :ilosc_max and wartosc > :wartosc_min and wartosc < :wartosc_max and data_zamowienia >= :data_zamowienia_od and data_zamowienia <= :data_zamowienia_do and status like :status')
			else:
				cur.prepare('select order_id, id_uzytkownika, id_produktu, ilosc, wartosc, status, data_zamowienia from zamowienia_NDOL where id_uzytkownika like :id_uzytkownika and id_produktu like :id_produktu and ilosc > :ilosc_min and ilosc < :ilosc_max and wartosc > :wartosc_min and wartosc < :wartosc_max and data_zamowienia >= :data_zamowienia_od and data_zamowienia <= :data_zamowienia_do and status like :status')
			cur.execute(None, {'status': order[0],
								'id_uzytkownika':order[1],
							   'id_produktu': order[2],
							   'ilosc_min': order[3],
							   'ilosc_max': order[4],
							   'wartosc_min': order[5],
							   'wartosc_max':order[6],
							   'data_zamowienia_od': order[7],
							   'data_zamowienia_do': order[8]})
			results = cur.fetchall()
			for i in range(len(results)):
				results[i] = list(results[i])
				results[i][-1] = results[i][-1].strftime('%d-%m-%Y %H:%M')
			print(results)
			context = {'results': results}
			cur.close()
			con.close()
			return render(request, 'user/findord.html', {'user': user, 'form': form, 'results': results, 'user_id': user_id})
	form = OrderForm()
	form.fields['id_uzytkownika'].widget = forms.HiddenInput()
	if 'order' in request.session:
		order = request.session['order']
		request.session['order'] = order
		order = list(order)
		order[-1] = datetime.strptime(order[-1], "%Y %m %d")
		order[-2] = datetime.strptime(order[-2], "%Y %m %d")
		print(order)
		con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
						cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
		cur = con.cursor()
		if request.session['_wojewodztwo_']=='Dolnośląskie':
			cur.prepare('select order_id, id_uzytkownika, id_produktu, ilosc, wartosc, status, data_zamowienia from zamowienia_DOL where id_uzytkownika like :id_uzytkownika and id_produktu like :id_produktu and ilosc > :ilosc_min and ilosc < :ilosc_max and wartosc > :wartosc_min and wartosc < :wartosc_max and data_zamowienia >= :data_zamowienia_od and data_zamowienia <= :data_zamowienia_do and status like :status')
		else:
			cur.prepare('select order_id, id_uzytkownika, id_produktu, ilosc, wartosc, status, data_zamowienia from zamowienia_NDOL where id_uzytkownika like :id_uzytkownika and id_produktu like :id_produktu and ilosc > :ilosc_min and ilosc < :ilosc_max and wartosc > :wartosc_min and wartosc < :wartosc_max and data_zamowienia >= :data_zamowienia_od and data_zamowienia <= :data_zamowienia_do and status like :status')
		cur.execute(None, {'status': order[0],
							'id_uzytkownika':order[1],
							'id_produktu': order[2],
						   'ilosc_min': order[3],
						   'ilosc_max': order[4],
						   'wartosc_min': order[5],
						   'wartosc_max':order[6],
						   'data_zamowienia_od': order[7],
						   'data_zamowienia_do': order[8]})
		results = cur.fetchall()
		for i in range(len(results)):
			results[i] = list(results[i])
			results[i][-1] = results[i][-1].strftime('%d-%m-%Y %H:%M')
		print(results)
		context = {'form': form, 'results': results}
		cur.close()
		con.close()
		#return render(request, TEMPLATE_PATHH+'findord.html', context)
	return render(request, 'user/findord.html', {'form': form, 'results': results, 'user': user, 'user_id': user_id})

def deleteOrderUser(request, user_id=None, order_id =None):
	request.session.modified = True
	request.session.set_expiry(900)
	if '_login_' not in request.session or request.session.get('_id', None)!=user_id:
		return HttpResponseRedirect(reverse('sklep:login'))
	user = request.session['_login_']
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	cur = con.cursor()
	cur.callproc('anuluj_zamowienie', (order_id, request.session['_wojewodztwo_']))
	cur.close()
	con.commit()
	con.close()
	return HttpResponseRedirect(reverse('sklep:findordUser', args=(user_id,)))

def listProdUser(request, user_id=None):
	request.session.modified = True
	request.session.set_expiry(900)
	print(request.session.get_session_cookie_age())
	if '_login_' not in request.session or request.session.get('_id', None)!=user_id:
		return HttpResponseRedirect(reverse('sklep:login'))
	user = request.session['_login_']
	con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
							cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
	print(con.version)
	cur = con.cursor()
	cur.execute('select * from produkty order by product_id')
	results = cur.fetchall()
	context = {'results': results, 'user':user, 'user_id': user_id }
	cur.close()
	con.close()
	return render(request, TEMPLATE_PATHH+'user/listProd.html', context)

def orderProdUser(request, user_id=None, prod_id=None):

	print(request.session.get_session_cookie_age())
	request.session.set_expiry(900)
	request.session.modified = True
	if '_login_' not in request.session or request.session.get('_id', None)!=user_id:
		return HttpResponseRedirect(reverse('sklep:login'))
	user = request.session['_login_']

	if request.method == 'POST':
		if 'ilosc' in request.POST:
			ilosc = request.POST['ilosc']
			print(ilosc)
			print(request.session['_wojewodztwo_'])
			con = cx_Oracle.connect('robert', 'qwerty', '192.168.56.1/orcl',
						cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
			print(con.version)
			cur = con.cursor()
			cur.callproc('dodaj_zamowienie', (user_id, prod_id, ilosc, request.session['_wojewodztwo_']))
			cur.close()
			con.close() 
	return HttpResponseRedirect(reverse('sklep:listprodUser', args=(user_id,)))

