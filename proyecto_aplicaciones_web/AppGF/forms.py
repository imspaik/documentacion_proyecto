from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AppGF.models import *
from django.forms import formset_factory
from oscar.apps.catalogue.models import Product

class Registro(UserCreationForm):
    provincia = forms.CharField(max_length=30, required=False, help_text='Optional.')
    localidad = forms.CharField(max_length=30, required=False, help_text='Optional.')
    experiencia = forms.CharField(widget=forms.Textarea, required=False)
    foto_de_perfil = forms.FileField(required=False)
    email = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'provincia', 'foto_de_perfil', 'localidad', 'experiencia', 'password1', 'password2',  )

class CrearCapturaForm(forms.Form):
	fecha_captura = forms.DateField(help_text="Fecha DD/MM/YYYY")
	pescado = forms.ModelChoiceField(queryset=Pescado.objects.all())
	cantidad = forms.IntegerField()
	carrete = forms.ModelChoiceField(queryset=Product.objects.filter(product_class=3))
	caña = forms.ModelChoiceField(queryset=Product.objects.filter(product_class=2))
	señuelo = forms.ModelChoiceField(queryset=Product.objects.filter(product_class=4))
	zona = forms.ModelChoiceField(queryset=ZonaPesca.objects.all())
	marea = forms.ModelChoiceField(queryset=Marea.objects.all())
	foto_captura = forms.FileField(required=False)

class ContactForm(forms.Form):
	nombre = forms.CharField()
	email = forms.EmailField()
	mensaje = forms.CharField(widget=forms.Textarea)	
	def clean_email(self):
		email = self.cleaned_data.get("email")
		email_base, proveeder = email.split("@")
		dominio, extension = proveeder.split(".")
		
		return email
		
	
