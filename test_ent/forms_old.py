# forms.py

from django import forms
from .models import calendar, client

class calendarForm(forms.ModelForm):
    class Meta:
        model = calendar
        fields = ['date', 'surname', 'name', 'address', 'city', 'phone', 'email', 'job_type', 'category', 'price', 'paid', 'comments', 'installation_manual']

class clientForm(forms.ModelForm):
    class Meta:
        model = client
        fields = ['surname', 'name', 'address', 'city', 'phone', 'email']
