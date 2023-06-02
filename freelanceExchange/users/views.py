from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from formtools.wizard.views import SessionWizardView
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

class MyStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        parts = name.split('.')
        basename = parts[0]
        ext = parts[-1]
        number = 1
        while self.exists(name):
            name = 'freelancers/resumes/%s_%d.%s' % (basename, number, ext)
            number += 1
        return name


# Create your views here.
def index(request):
    try:
        freelancer = request.user.profile.freelancer
    except:
        freelancer = request.user
        print(freelancer)

    return render(request, 'users/index.html', {'user': request.user, 'freelancer': freelancer})


class RegisterWizard(SessionWizardView):
    template_name = 'users/register_form.html'
    done_template = 'users/index.html'
    success_url = reverse_lazy('index')
    form_list = [RoleForm, RegisterForm2]

    def done(self, form_list, **kwargs):
        username = form_list[1].cleaned_data['email']
        first_name = form_list[1].cleaned_data['first_name']
        last_name = form_list[1].cleaned_data['last_name']
        email = form_list[1].cleaned_data['email']
        password = form_list[1].cleaned_data['password1']

        # complete the registration process
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        login(self.request, user)
        profile = self.request.user.profile
        profile.role = Role.objects.get(name=form_list[0].cleaned_data['role'])
        profile.save()
        if form_list[0].cleaned_data['role'] == 'freelancer':
            freelancer = Freelancer.objects.create(owner=profile)
            freelancer.save()
            return redirect('freelancer_login')
        else:
            customer = Customer.objects.create(owner=profile)
            customer.save()
            return redirect('task_add')
        return redirect('index')


class FreelanceLogin(SessionWizardView):
    template_name = 'users/freelance_login.html'
    done_template = 'users/index.html'
    success_url = reverse_lazy('index')
    form_list = [FreelanceForm1, FreelanceForm2, LanguageForm, EducationForm, ExperienceForm, FreelanceForm3, ]
    file_storage = MyStorage()

    def done(self, form_list, **kwargs):
        user = self.request.user.profile.freelancer
        language = Language.objects.create(
            owner=user,
            level=form_list[2].cleaned_data['level'],
            language=form_list[2].cleaned_data['language']
        )
        language.save()
        education = Education.objects.create(
            owner=user,
            level=form_list[3].cleaned_data['level'],
            institution=form_list[3].cleaned_data['institution'],
            faculty=form_list[3].cleaned_data['faculty'],
            major=form_list[3].cleaned_data['major'],
            start_training=form_list[3].cleaned_data['start_training'],
            end_training=form_list[3].cleaned_data['end_training'],
        )
        education.save()
        experience = Experience.objects.create(
            owner=user,
            organization=form_list[4].cleaned_data['organization'],
            post=form_list[4].cleaned_data['post'],
            duties=form_list[4].cleaned_data['duties'],
            start_work=form_list[4].cleaned_data['start_work'],
            end_work=form_list[4].cleaned_data['end_work']
        )
        experience.save()
        user.experiences_for_freelance = form_list[0].cleaned_data['experiences_for_freelance']
        user.bio = form_list[5].cleaned_data['bio']
        user.resume = form_list[1].cleaned_data['resume']
        user.save()
        return redirect('serves_add')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "Такого пользователя не существует")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Почта или пароль были введены не корректно")
    return render(request, 'users/login_user.html')


def logout_user(request):
    logout(request)

    return redirect('index')


def serves_add(request):
    user = request.user.profile.freelancer
    if request.method == 'POST':
        serves = request.POST.getlist('service')
        user.serves.set(serves)
        return redirect('talent_add')
    context = {'service': Services.objects.all()}
    return render(request, 'users/serves_add.html', context)


def profile_update(request):
    profile = request.user.profile
    print(profile)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print('POST true')
        if form.is_valid():
            print('is valid')
            form.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)
