from django import forms
from .models import *
from django.forms import ModelForm
from .utils import EXPERIENCE, AMOUNT_OF_WORK


class TaskTitleForm(forms.Form):
    title = forms.CharField(max_length=200, label='', widget=forms.TextInput(attrs={'class': 'reg_form'}))


class TaskSkillForm(forms.Form):
    skills = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                            queryset=Skills.objects.all(),
                                            required=False, label='')


class AmountOfWorkForm(forms.Form):
    amount = forms.ChoiceField(choices=AMOUNT_OF_WORK, widget=forms.Select(attrs={'class': 'reg_form'}),
                               label='Оцените объем своей работы')
    experience = forms.ChoiceField(choices=EXPERIENCE, widget=forms.Select(attrs={'class': 'reg_form'}),
                                   label='Какой уровень работы для этого требуется?')
    contract_work = forms.BooleanField(required=False, label='Является ли эта работа возможностью найма по контракту?')


class DescriptionForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'reg_form_text', 'placeholder': 'Описание уже есть? Вставьте его здесь!'}, ),
        label='')


class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'
        exclude = ['owner']
        labels = {
            'name': 'Какой будет бюджет',
            'min_price': 'От',
            'max_price': 'До',
            'fix_price': 'Максимальный бюджет проекта'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'reg_form'})
