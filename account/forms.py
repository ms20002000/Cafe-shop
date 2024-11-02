from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='شماره تلفن',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'شماره تلفن خود را وارد کنید'
        })
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور خود را وارد کنید'
        })
    )


class StaffAddForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'first_name', 'last_name', 'specialty', 'is_staff','email', 'profile_picture']