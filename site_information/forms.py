from django import forms
from .models import SiteInfo

class SiteInfoForm(forms.ModelForm):
    class Meta:
        model = SiteInfo
        fields = ['site_name', 'logo', 'phone_number', 'email', 'address', 'description']
