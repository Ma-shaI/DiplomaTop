from django.forms import ModelForm
from .models import *
from django import forms


class TalentForm(ModelForm):
    is_published = forms.BooleanField(required=False, label='Опубликовать')
    descriptions = forms.CharField(widget=forms.Textarea(), required=False, label='Расскажите о вашем опыте')
    class Meta:
        model = Talent
        fields = ['service', 'title', 'descriptions', 'hourly_rate', 'skills', 'is_published']
        labels = {'service': 'Выберите специальность',
                  'title': 'Ваш заголовок',

                  'hourly_rate': 'Определите почасовую оплату',
                  'skills': 'Выберите свои навыки и опыт'
                  }
        widgets = {'service': forms.Select(), 'skills': forms.CheckboxSelectMultiple(),

                }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'skills':
                field.widget.attrs.update({'class': 'form_checkbox'})
            else:
                field.widget.attrs.update({'class': 'reg_form'})
