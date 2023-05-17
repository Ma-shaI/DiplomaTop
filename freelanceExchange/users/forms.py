from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django import forms
from tasks.models import Task


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Введите пароль'
        self.fields['password2'].label = 'Повторите пароль'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'last_name': "Фамилия",
            'email': "Почта"
        }
#
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #
#     #     for name, field in self.fields.items():
#     #         field.widget.attrs.update({'class': 'input'})
#
#
# class FreelanceCreationForm(ModelForm):
#     class Meta:
#         model = Freelancer
#         fields = ['experiences', 'resume', 'profile_image', 'bio', 'hourly_rate', 'serves']
#         labels = {
#             'experiences': " Есть ли у вас опыт во фрилансе",
#             'resume': "Загрузите ваше резюме",
#             'profile_image': "Загрузите фото, которое будет отображаться в вашем профиле",
#             'bio': "Расскажите о себе",
#             'hourly_rate': "Ваша почасовая ставка",
#             'serves': 'В какой сфере вы предоставляете услуги'
#         }
#         widgets = {'experiences': forms.RadioSelect(),
#                    'serves': forms.CheckboxSelectMultiple()
#                    }
#
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #
#     #     for name, field in self.fields.items():
#     #         field.widget.attrs.update({'class': 'input'})
#
#
# class LanguageForm(ModelForm):
#     class Meta:
#         model = Language
#         fields = ['language', 'level']
#         labels = {
#             'language': 'Выберите язык, которым вы владеете',
#             'level': 'Ваш уровень владения языком'
#         }
#
#
# class CustomerForm(ModelForm):
#     model = Customer
#     fields = '__all__'
#     exclude = ['created']
#
#
# class TaskForm(ModelForm):
#     model = Task
#     fields = '__all__'
#     exclude = ['owner', 'time_created', 'time_updated']
