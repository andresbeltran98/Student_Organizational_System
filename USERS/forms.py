from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    university = forms.CharField(max_length=50, required=True)
    major = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'university', 'major', 'password1', 'password2']
