from django.forms import ModelForm
from .models import *
from django import forms
from .utils import CURRENCY


class TalentForm(forms.Form):
    service = forms.ModelMultipleChoiceField(widget=forms.Select(attrs={'class': 'form_select'}),
                                             queryset=Services.objects.all(),
                                             required=False, label='Выберите специальность')
    title = forms.CharField(label='Ваш заголовок', widget=forms.TextInput(attrs={'class': 'reg_form'}))
    descriptions = forms.CharField(widget=forms.Textarea(attrs={'class': 'reg_form'}), required=False,
                                   label='Расскажите о вашем опыте')
    skills = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'reg_form'}),
                                            queryset=Skills.objects.all(),
                                            required=False, label='Добавьте свои навыки')
    rate = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'reg_form_rate'}), label='Почасовая ставка')
    currency = forms.ChoiceField(widget=forms.Select(attrs={'class': 'reg_form_currency'}), choices=CURRENCY, label='Валюта')
    is_published = forms.BooleanField(required=False, label='Опубликовать')
