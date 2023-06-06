from django import forms
from .models import *
from django.forms import ModelForm
from .utils import LANGUAGE, LEVEL
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


class RoleForm(forms.Form):
    ROLE = (('client', 'Я клиент, нанимаю для проекта'), ('freelancer', 'Я фрилансер, ищу работу'))
    role = forms.ChoiceField(choices=ROLE, label='', widget=forms.RadioSelect(attrs={'class': 'role'}))


class RegisterForm2(forms.Form):
    first_name = forms.CharField(label='', max_length=200,
                                 widget=forms.TextInput(attrs={'class': 'reg_form', 'placeholder': 'Ваше имя', }))
    last_name = forms.CharField(label='', max_length=250,
                                widget=forms.TextInput(attrs={'class': 'reg_form', 'placeholder': 'Ваша фамилия'}))
    email = forms.EmailField(label='',
                             widget=forms.TextInput(
                                 attrs={'class': 'reg_form', 'placeholder': 'Адрес электронной почты'}))
    password1 = forms.CharField(label='',
                                widget=forms.PasswordInput(attrs={'class': 'reg_form', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'reg_form', 'placeholder': 'Повторите пароль'}))


class FreelanceForm1(forms.Form):
    EXPERIENCE = (
        ('junior', 'Я новичок'),
        ('middle', 'У меня есть некоторый опыт'),
        ('senior', 'Я эксперт')
    )
    experiences_for_freelance = forms.ChoiceField(label='', choices=EXPERIENCE,
                                                  widget=forms.RadioSelect(attrs={'class': 'freelance_experience'}))


class FreelanceForm2(forms.Form):
    resume = forms.FileField(widget=forms.ClearableFileInput(), required=False, label='')


class FreelanceForm3(forms.Form):
    bio = forms.CharField(label='', required=False,
                          widget=forms.Textarea(attrs={'class': 'reg_form_text',
                                                       'placeholder': 'Расскажите о своих основных навыках, опыте и интересах'}))


class EducationForm(forms.Form):
    LEVEL = (('', ''),
             ('secondary', 'Среднее'),
             ('special_secondary', 'Среднее специальное'),
             ('unfinished_higher', 'Неоконченное высшее'),
             ('higher', 'Высшее'),
             ('bachelor', 'Бакалавр'),
             ('master', 'Магистр'),
             ('candidate', 'Кандидат наук'),
             ('doctor', 'Доктор наук'),)
    level = forms.ChoiceField(choices=LEVEL, label='Уровень',
                              widget=forms.Select(attrs={'class': 'reg_form'}), initial='',
                              required=False)
    institution = forms.CharField(max_length=300, label='Учебное заведение',
                                  widget=forms.TextInput(attrs={'class': 'reg_form'}), required=False)
    faculty = forms.CharField(max_length=250, label='Факультет', widget=forms.TextInput(attrs={'class': 'reg_form'}),
                              required=False)
    major = forms.CharField(max_length=355, label='Специализация', widget=forms.TextInput(attrs={'class': 'reg_form'}),
                            required=False)
    start_training = forms.IntegerField(label='Год начала обучения',
                                        widget=forms.TextInput(attrs={'class': 'reg_form'}), required=False)
    end_training = forms.IntegerField(label='Год окончания', widget=forms.TextInput(attrs={'class': 'reg_form'}),
                                      required=False)


class ExperienceForm(forms.Form):
    organization = forms.CharField(max_length=250, label='Огранизация',
                                   widget=forms.TextInput(attrs={'class': 'reg_form'}), required=False)
    post = forms.CharField(max_length=250, label='Должность', widget=forms.TextInput(attrs={'class': 'reg_form'}),
                           required=False)
    duties = forms.CharField(label='Рабочие обязанности', widget=forms.Textarea(attrs={'class': 'reg_form'}),
                             required=False)
    start_work = forms.IntegerField(label='Дата начала', widget=forms.TextInput(attrs={'class': 'reg_form'}),
                                    required=False)
    end_work = forms.IntegerField(label='Дата окончания', widget=forms.TextInput(attrs={'class': 'reg_form'}),
                                  required=False)


class LanguageForm(forms.Form):
    language = forms.ChoiceField(choices=LANGUAGE, label='Язык', widget=forms.Select(attrs={'class': 'reg_form'}),
                                 required=False)
    level = forms.ChoiceField(choices=LEVEL, label='Мой уровень', widget=forms.Select(attrs={'class': 'reg_form'}),
                              initial='',
                              required=False)

    def __init__(self, *args, **kwargs):
        initial_language = kwargs.pop('initial_language', 'eng')
        super(LanguageForm, self).__init__(*args, **kwargs)
        self.fields['language'].initial = initial_language


class ProfileForm(ModelForm):
    phone_number = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget(), label='Номер телефона')
    second_number = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget(), required=False,
                                     label='Дополнительный номер телефона')

    class Meta:
        model = Profile
        fields = ['photo', 'country', 'city', 'phone_number', 'second_number']
        labels = {
            'photo': 'Ваше фото',
            'country': 'Страна ',
            'city': 'Город',
            'phone_number': 'Номер телефона',

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'reg_form'})
