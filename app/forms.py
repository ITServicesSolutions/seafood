from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import *
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class CreationUserForm(UserCreationForm):
    class Meta:
        model = User
        fields=('username','email','password1','password2')

class ClientForm(ModelForm):
    mobile = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='BJ')
        )
    class Meta:
        model = Client
        fields = ('nom', 'prenom', 'entreprise', 'mobile')
        exclude=['user']

class AddressForm(ModelForm):
    class Meta:
        model = Adresse
        fields = ('adresse', 'ville','quartier', 'code_postal')
        exclude=['user.client']

class QuantiteForm(forms.Form):
    quantite = forms.CharField(max_length=4)
    
    
