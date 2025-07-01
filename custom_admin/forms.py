from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'w-full px-4 py-2 border rounded mt-1',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded mt-1',
            'placeholder': 'Password'
        })
    )
