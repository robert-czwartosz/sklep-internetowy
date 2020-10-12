from django import forms
import datetime


WOJEWODZTWA = ['','Dolnośląskie', 'Kujawsko-pomorskie', 
'Lubelskie', 'Lubuskie','Łódzkie','Małopolskie',
'Mazowieckie','Opolskie','Podkarpackie',
'Podlaskie','Pomorskie','Śląskie','Świętokrzyskie',
'Warmińsko-mazurskie','Wielkopolskie','Zachodniopomorskie']
WOJEWODZTWA = [(X,X) for X in WOJEWODZTWA]

class SignUpForm(forms.Form):
	login = forms.CharField(min_length=8, max_length=50)
	haslo = forms.CharField(label="Hasło",min_length=8, max_length=50, widget=forms.PasswordInput())
	haslo_ = forms.CharField(label="Powtórz hasło", min_length=8, max_length=50, widget=forms.PasswordInput())
	imie = forms.CharField(label="Imię", max_length=50)
	nazwisko = forms.CharField(max_length=50)
	wojewodztwo = forms.ChoiceField(required=True, choices=WOJEWODZTWA[1:], label="Województwo")
	miasto = forms.CharField(max_length=50)
	kod_pocztowy = forms.CharField(max_length=50)
	ulica = forms.CharField(max_length=50)
	nr_domu = forms.CharField(max_length=10)
	telefon = forms.IntegerField(max_value=999999999999, min_value=0, localize=True)
	email = forms.EmailField(max_length=50)
	"""message = forms.CharField(
		max_length=2000,
		widget=forms.Textarea(),
		help_text='Write here your message!'
	)
	source = forms.CharField(       # A hidden input for internal use
		max_length=50,              # tell from which page the user sent the message
		widget=forms.HiddenInput()
	)"""
	def clean(self):
		cleaned_data = super(SignUpForm, self).clean()
		login = cleaned_data.get('login')
		haslo = cleaned_data.get('haslo')
		haslo_ = cleaned_data.get('haslo_')
		imie = cleaned_data.get('imie')
		nazwisko = cleaned_data.get('nazwisko')
		wojewodztwo = cleaned_data.get('wojewodztwo')
		miasto = cleaned_data.get('miasto')
		kod_pocztowy = cleaned_data.get('kod_pocztowy')
		ulica = cleaned_data.get('ulica')
		nr_domu = cleaned_data.get('nr_domu')
		telefon = cleaned_data.get('telefon')
		email = cleaned_data.get('email')
		if not login:
			raise forms.ValidationError('Field login is required!')
		if not haslo:
			raise forms.ValidationError('Field haslo is required!')
		if not haslo==haslo_:
			raise forms.ValidationError('Passwords in both fields should be the same!')
		if not imie:
			raise forms.ValidationError('Field imie is required!')
		if not nazwisko:
			raise forms.ValidationError('Podaj nazwisko!')
		if not wojewodztwo:
			raise forms.ValidationError('Field wojewodztwo is required!')
		if not miasto:
			raise forms.ValidationError('Field miasto is required!')
		if not kod_pocztowy:
			raise forms.ValidationError('Field kod_pocztowy is required!')
		if not ulica:
			raise forms.ValidationError('Field ulica is required!')
		if not nr_domu:
			raise forms.ValidationError('Field nr_domu is required!')
		if not telefon:
			raise forms.ValidationError('Podaj nr telefonu!')
		if not email:
			raise forms.ValidationError('Podaj email!')


class LoginForm(forms.Form):
	login = forms.CharField(min_length=8, max_length=50)
	haslo = forms.CharField(label="Hasło",min_length=8, max_length=50, widget=forms.PasswordInput())
	
	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		login = cleaned_data.get('login')
		haslo = cleaned_data.get('haslo')
		if not login:
			raise forms.ValidationError('Field login is required!')
		if not haslo:
			raise forms.ValidationError('Field haslo is required!')

class UserForm(forms.Form):
	login = forms.CharField(max_length=50, required=False)
	imie = forms.CharField(label='Imię', max_length=50, required=False)
	nazwisko = forms.CharField(max_length=50, required=False)
	wojewodztwo = forms.ChoiceField(required=False, choices=WOJEWODZTWA, label="Województwo")
	miasto = forms.CharField(max_length=50, required=False)
	kod_pocztowy = forms.CharField(max_length=50, required=False)
	ulica = forms.CharField(max_length=50, required=False)
	nr_domu = forms.CharField(max_length=10, required=False)
	telefon = forms.IntegerField(max_value=999999999999, min_value=0, localize=True, required=False)
	email = forms.EmailField(max_length=50, required=False)
	
	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		login = cleaned_data.get('login')
		imie = cleaned_data.get('imie')
		nazwisko = cleaned_data.get('nazwisko')
		wojewodztwo = cleaned_data.get('wojewodztwo')
		miasto = cleaned_data.get('miasto')
		kod_pocztowy = cleaned_data.get('kod_pocztowy')
		ulica = cleaned_data.get('ulica')
		nr_domu = cleaned_data.get('nr_domu')
		telefon = cleaned_data.get('telefon')
		email = cleaned_data.get('email')
		if not login:
			login = ''
			#raise forms.ValidationError('Field login is required!')
		if not imie:
			imie = ''
			#raise forms.ValidationError('Field imie is required!')
		if not nazwisko:
			#raise forms.ValidationError('Podaj nazwisko!')
			nazwisko = ''
		if not wojewodztwo:
			wojewodztwo = ''
			#raise forms.ValidationError('Field wojewodztwo is required!')
		if not miasto:
			miasto = ''
			#raise forms.ValidationError('Field miasto is required!')
		if not kod_pocztowy:
			kod_pocztowy = ''
			#raise forms.ValidationError('Field kod_pocztowy is required!')
		if not ulica:
			ulica =''
			#raise forms.ValidationError('Field ulica is required!')
		if not nr_domu:
			nr_domu = ''
			#raise forms.ValidationError('Field nr_domu is required!')
		if not telefon or telefon==None:
			telefon = ''
			#raise forms.ValidationError('Podaj nr telefonu!')
		if not email:
			email = ''
			#raise forms.ValidationError('Podaj email!')"""


class ProductForm(forms.Form):
	nazwa = forms.CharField(max_length=100)
	ilosc = forms.IntegerField(label='Ilość', min_value=0, localize=True)
	cena = forms.FloatField(localize=True)
	opis = forms.CharField(max_length=1024,
						   widget=forms.Textarea(),
							help_text='Opis produktu.')

	def clean(self):
		cleaned_data = super(ProductForm, self).clean()
		nazwa = cleaned_data.get('nazwa')
		ilosc = cleaned_data.get('ilosc')
		cena = cleaned_data.get('cena')
		opis = cleaned_data.get('opis')
		if not nazwa:
			raise forms.ValidationError('Field login is required!')
		if not ilosc:
			raise forms.ValidationError('Field ilosc is required!')
		if not cena:
			raise forms.ValidationError('Field cena is required!')
		if not opis:
			raise forms.ValidationError('Field opis is required!')

STATUS_LIST = ['','Wykonane', 'Realizowane', 'Przyjęte']
STATUS_LIST = [(X,X) for X in STATUS_LIST]
class OrderForm(forms.Form):
	status = forms.ChoiceField(required=False, choices=STATUS_LIST)
	id_uzytkownika = forms.IntegerField(label='ID Użytkownika', min_value=0, localize=True, required=False)
	id_produktu = forms.IntegerField(label='ID Produktu', min_value=0, localize=True, required=False)
	ilosc_min = forms.IntegerField(label='Ilość min.', min_value=0, localize=True, required=True, initial=0)
	ilosc_max = forms.IntegerField(label='Ilość maks.', min_value=0, localize=True, required=True, initial=2**30)
	wartosc_min = forms.FloatField(label='Wartość min.', localize=True, required=True, initial=0)
	wartosc_max = forms.FloatField(label='Wartość maks.', localize=True, required=True, initial=2**30)
	data_zamowienia_od = forms.DateField(label='Data zamówienia (od)', required=False, widget=forms.SelectDateWidget(years=range(2000,2100)))
	data_zamowienia_do = forms.DateField(label='Data zamówienia (do)', required=False, widget=forms.SelectDateWidget(years=range(2000,2100)))
	
	def clean(self):
		cleaned_data = super(OrderForm, self).clean()
		status = cleaned_data.get('status')
		id_uzytkownika = cleaned_data.get('id_uzytkownika')
		id_produktu = cleaned_data.get('id_produktu')
		ilosc_min = cleaned_data.get('ilosc_min')
		ilosc_max = cleaned_data.get('ilosc_max')
		wartosc_min = cleaned_data.get('wartosc_min')
		wartosc_max = cleaned_data.get('wartosc_max')
		data_zamowienia_od = cleaned_data.get('data_zamowienia_od')
		data_zamowienia_do = cleaned_data.get('data_zamowienia_do')


class EmpForm(forms.Form):
	imie = forms.CharField(label='Imię', max_length=50)
	nazwisko = forms.CharField(max_length=50)
	pesel = forms.IntegerField(min_value=0, max_value=99999999999, localize=True)
	stanowisko = forms.CharField(max_length=50)
	wynagrodzenie = forms.FloatField(localize=True)

	def clean(self):
		cleaned_data = super(EmpForm, self).clean()
		imie = cleaned_data.get('imie')
		nazwisko = cleaned_data.get('nazwisko')
		pesel = cleaned_data.get('pesel')
		stanowisko = cleaned_data.get('stanowisko')
		wynagrodzenie = cleaned_data.get('wynagrodzenie')
		if not imie:
			raise forms.ValidationError('Field imie is required!')
		if not nazwisko:
			raise forms.ValidationError('Field nazwisko is required!')
		if not pesel:
			raise forms.ValidationError('Field pesel is required!')
		if not stanowisko:
			raise forms.ValidationError('Field stanowisko is required!')
		if not wynagrodzenie:
			raise forms.ValidationError('Field wynagrodzenie is required!')
