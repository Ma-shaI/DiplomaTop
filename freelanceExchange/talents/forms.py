from django.forms import ModelForm
from .models import *
from django import forms


class TalentForm(ModelForm):
    class Meta:
        model = Talent
        fields = ['service', 'title', 'descriptions', 'hourly_rate', 'is_published', 'skills']
        widgets = {'service': forms.Select(), 'skills': forms.CheckboxSelectMultiple()}
