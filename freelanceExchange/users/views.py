from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from formtools.wizard.views import SessionWizardView
from django.urls import reverse_lazy
from django.contrib.auth import logout, login


# Create your views here.
def index(request):
    return render(request, 'users/index.html', {'user': request.user})


class RegisterWizard(SessionWizardView):
    template_name = 'users/register_form.html'
    done_template = 'users/index.html'
    success_url = reverse_lazy('index')
    form_list = [RoleForm, RegisterForm2]

    def done(self, form_list, **kwargs):
        username = f"{form_list[1].cleaned_data['first_name']}_{form_list[1].cleaned_data['last_name']}"
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
        return redirect('index')


def logout_user(request):
    logout(request)

    return redirect('index')

