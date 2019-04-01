from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class UserSignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Username'}
    ), required=True, max_length=50)

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Enter your email'}
    ), required=True, max_length=50)

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Password'}
    ), required=True, max_length=50)

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Conform Password'}
    ), required=True, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']