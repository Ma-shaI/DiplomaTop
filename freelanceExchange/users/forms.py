from django import forms
from .models import *

class RoleForm(forms.Form):
    ROLE = (('client', 'Клиент'), ('freelancer', 'Фрилансер'))
    role = forms.ChoiceField(choices=ROLE, widget=forms.RadioSelect())


class RegisterForm2(forms.Form):
    first_name = forms.CharField(label='Ваше имя', max_length=200)
    last_name = forms.CharField(label='Ваша фамилия', max_length=250)
    email = forms.EmailField(label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())


class FreelanceForm1(forms.Form):
    EXPERIENCE = (
        ('junior', 'Я новичок'),
        ('middle', 'У меня есть некоторый опыт'),
        ('senior', 'Я эксперт')
    )
    experiences_for_freelance = forms.ChoiceField(choices=EXPERIENCE, widget=forms.RadioSelect())


class EducationForm(forms.Form):
    LEVEL = (('secondary', 'Среднее'),
             ('special_secondary', 'Среднее специальное'),
             ('unfinished_higher', 'Неоконченное высшее'),
             ('higher', 'Высшее'),
             ('bachelor', 'Бакалавр'),
             ('master', 'Магистр'),
             ('candidate', 'Кандидат наук'),
             ('doctor', 'Доктор наук'),)
    level = forms.ChoiceField(choices=LEVEL)
    institution = forms.CharField(max_length=300)
    faculty = forms.CharField(max_length=250)
    major = forms.CharField(max_length=355)
    year = forms.DateTimeField()


class FreelanceForm2(forms.Form):
    bio = forms.CharField(widget=forms.Textarea)



class ServicesForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Services.objects.all())
