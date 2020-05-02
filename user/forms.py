from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ProfilePic
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
		
class UserProfileEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email']
		
		widgets = {
			'username':forms.TextInput(attrs = {
				'class':'form-control',
				'placeholder':'Username',
			}),
			'email':forms.EmailInput(attrs = {
				'class':'form-control',
				'placeholder':'Email',
			}),
			'first_name':forms.TextInput(attrs = {
				'class':'form-control',
				'placeholder':'First Name',
			}),
			'last_name':forms.TextInput(attrs = {
				'class':'form-control',
				'placeholder':'Last Name',
			}),
		}

class ProfilePicEditForm(forms.ModelForm):
	class Meta:
		model = ProfilePic
		fields = ['profile']
		widgets = {
			'profile': forms.FileInput(attrs = {
				'class':'custom-file-input',
			})
		}
		required  = {
			'profile':False,
		}