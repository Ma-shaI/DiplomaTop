from django.forms import ModelForm
from .models import *
from django import forms

CURRENCY = (
    ('ruble', '₽'),
    ('dollar', '$'),
    ('euro', '€')
)


class TalentForm(forms.Form):
    service = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form_select'}),
                                     queryset=Services.objects.all(),
                                     required=False, label='Выберите специальность')
    title = forms.CharField(label='Ваш заголовок', widget=forms.TextInput(attrs={'class': 'reg_form'}),
                            required=False, )
    descriptions = forms.CharField(widget=forms.Textarea(attrs={'class': 'reg_form'}), required=False,
                                   label='Расскажите о вашем опыте')
    skills = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'reg_form'}),
                                            queryset=Skills.objects.all(),
                                            required=False, label='Добавьте свои навыки')
    rate = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'reg_form_rate'}), label='Почасовая ставка',
                              required=False)
    currency = forms.ChoiceField(widget=forms.Select(attrs={'class': 'reg_form_currency'}), choices=CURRENCY,
                                 label='Валюта', required=False, )
    is_published = forms.BooleanField(required=False, label='Опубликовать')


class TalentUpdateForm(ModelForm):
    class Meta:
        model = Talent
        fields = '__all__'
        exclude = ['owner', 'customer_saved', 'customer_invited']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'reg_form'})


class RateForm(ModelForm):
    rate = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'reg_form_rate'}), label='Почасовая ставка',
                              required=False)
    currency = forms.ChoiceField(widget=forms.Select(attrs={'class': 'reg_form_currency'}), choices=CURRENCY,
                                 label='Валюта', required=False, )

    class Meta:
        model = HourlyRate
        fields = '__all__'
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
