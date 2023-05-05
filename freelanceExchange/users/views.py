from django.shortcuts import render, redirect
from .forms import FreelanceCreationForm, CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def register_user(request):
    if request.method == 'POST':
        if request.POST['reg'] == 'client':
            return redirect('reg_start_client')
        elif request.POST['reg'] == 'freelancer':
            return redirect('reg_start_frlnc')
    return render(request, 'users/register_user.html')


def reg_start_client(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = f'{user.first_name}_{user.last_name}'
            user.save()
            login(request, user)
            print('TRUUUUEEE clietn')
            return redirect('reg_client')
        else:
            print('FAAAALSE CLIENT')
            messages.error(request, 'Ошибка при регистрации')
    print('что-то пошло не так CLIENT')
    context = {
        'form': form,
        'reg': 'client'
    }
    return render(request, 'users/register.html', context)


def reg_client(request):
    return render(request, 'users/reg_client.html')


def reg_start_frlnc(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = f'{user.first_name}_{user.last_name}'
            user.save()
            login(request, user)
            print('TRUUUUEEE')
            return redirect('reg_freelancer')
        else:
            print('FAAALSEEE')
            messages.error(request, 'Ошибка при регистрации')
    context = {
        'form': form,
        'reg': 'freelancer'
    }
    return render(request, 'users/register.html', context)


def reg_freelancer(request):
    form = FreelanceCreationForm()
    if request.method == 'POST':
        form = FreelanceCreationForm(request.POST)
        if form.is_valid():
            freelancer = form.save(commit=False)
            freelancer.first_name = request.user.first_name
            freelancer.last_name = request.user.last_name
            freelancer.email = request.user.email
            freelancer.username = request.user.username
            freelancer.save()
            messages.success(request, 'Аккаунт фрилансера был создан')
            login(request, freelancer)
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации фрилансера')
    return render(request, 'users/reg_freelancer.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, 'Пользователь с таким логином не найден')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Логин или пароль введены некорректно')

    return render(request, 'users/login_user.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('login_user')