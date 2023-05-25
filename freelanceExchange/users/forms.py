from django import forms


class RoleForm(forms.Form):
    ROLE = (('client', 'Клиент'), ('freelancer', 'Фрилансер'))
    role = forms.ChoiceField(choices=ROLE, widget=forms.RadioSelect())


class RegisterForm2(forms.Form):
    first_name = forms.CharField(label='Ваше имя', max_length=200)
    last_name = forms.CharField(label='Ваша фамилия', max_length=250)
    email = forms.EmailField(label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())