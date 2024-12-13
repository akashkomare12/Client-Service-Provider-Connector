from django import forms
from .models import Client

class UpdateClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'mobile', 'city', 'pincode']
