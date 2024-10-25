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

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'profile_picture']
        

class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'specialty', 'loyalty_points',
                   'is_admin', 'is_staff', 'is_customer', 'is_active', 'is_superuser', 'profile_picture']