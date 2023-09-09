from django import forms
from .models import Client, Calendar

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['surname', 'name', 'address', 'city', 'phone', 'email', 'comments']

class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['date', 'job_type', 'category', 'price', 'paid', 'comments', 'installation_manual']
