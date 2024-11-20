from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'profile_picture']
        

class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'specialty', 'loyalty_points',
                   'is_admin', 'is_staff', 'is_customer', 'is_active', 'is_superuser', 'profile_picture']