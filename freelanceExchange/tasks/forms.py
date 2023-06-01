from django import forms
from .models import *
from django.forms import ModelForm
from .utils import EXPERIENCE, AMOUNT_OF_WORK


class TaskTitleForm(forms.Form):
    title = forms.CharField(max_length=200)


class TaskSkillForm(forms.Form):
    skills = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            queryset=Skills.objects.all(),
                                            required=False)


class AmountOfWorkForm(forms.Form):
    amount = forms.ChoiceField(choices=AMOUNT_OF_WORK, widget=forms.RadioSelect())
    experience = forms.ChoiceField(choices=EXPERIENCE)
    contract_work = forms.BooleanField()


class DescriptionForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea())


class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'
        exclude = ['owner']
        widget = {'name': forms.RadioSelect()}

