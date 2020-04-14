from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'email' : forms.TextInput(attrs = {
                'class':'form-control',
                'required':'true',
                'type':'email',
            }),
            'password' : forms.TextInput(attrs = {
                'class':'form-control',
                'required':'true',
                'type':'password',
            }),
            'username' : forms.TextInput(attrs = {
                'class':'form-control',
                'required':'true',
                'type':'text',
            }),
        }