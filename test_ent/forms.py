# forms.py

from django import forms
from .models import Calendar, Client

class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ['date', 'surname', 'name', 'address', 'city', 'phone', 'email', 'job_type', 'category', 'price', 'paid', 'comments', 'installationManual']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['surname', 'name', 'address', 'city', 'phone', 'email']
