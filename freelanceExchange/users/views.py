from django.shortcuts import render, redirect
from .forms import FreelanceCreationForm, CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


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
    return render(request, 'users/reg_start_client.html', {'form': form})


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
    print('что-то пошло не tak freelancer')
    return render(request, 'users/reg_start_frlnc.html', {'form': form})


def reg_freelancer(request):
    form = FreelanceCreationForm()
    if request.method == 'POST':
        form = FreelanceCreationForm(request.POST)
        if form.is_valid():
            print('TRUE')
        else:
            messages.error(request, 'Ошибка')
    return render(request, 'users/reg_freelancer.html', {'form': form})
