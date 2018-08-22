from django import forms
from apps.user.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField

UserModel = get_user_model()

class RegistroForm(UserCreationForm):

	password1 = forms.CharField(
		label= 'Contraseña',
		strip=False,
		widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Ingrese Contraseña', 'required':""}),
	)
	password2 = forms.CharField(
		label= 'Confirme Contraseña',
		widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Ingrese Contraseña De Nuevo', 'required':""}),
		strip=False,
	)

	class Meta:
		model = User
		fields = ['first_name','last_name','birthday','phone','email']
		labels = {
			'first_name': 'Nombre',
			'last_name': 'Apellido',
			'birthday': 'Fecha de Nacimiento',
			'email': 'Correo Electronico',
			'phone': 'Número Telefonico',
		}
		widgets = {
			'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese Nombre', 'required':""}),
			'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese Apellido', 'required':""}),
			'birthday': forms.DateInput(attrs={'class':'form-control', 'type':'date','placeholder':'Fecha de nacimiento','max':User().my_age(),'min':User().my_age(edad=False)}),
			'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Correo Electrónico', 'required':""}),
			'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese Número Telefonico'}),
		}

class Aute(AuthenticationForm):
	username = UsernameField(
		widget=forms.EmailInput(attrs={'type':'email','class':'form-control', 'placeholder':'Correo electronico', 'required':"", 'autofocus': True})
	)
	password = forms.CharField(
		label="Password",
		strip=False,
		widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña', 'required':""}),
	)

	error_messages = {
		'invalid_login': 'Password or Invalid Mail.',
		'inactive': 'This account is inactive.',
	}