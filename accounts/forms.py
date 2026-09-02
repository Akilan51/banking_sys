from django import forms
from django.contrib.auth.models import User
from .models import Customer


class RegisterForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput)

    phone=forms.CharField(max_length=15)

    address=forms.CharField(widget=forms.Textarea)

    aadhaar=forms.CharField(max_length=12)

    class Meta:

        model=User

        fields=[
            "username",
            "first_name",
            "last_name",
            "email",
            "password"
        ]