from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from formtools.wizard.views import SessionWizardView
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from talents.models import *
from django.db.models import Q
from django.db.models import Max, Count, Case, When, F, Value, CharField, IntegerField


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


def index(request):
    try:
        freelancer = request.user.profile.freelancer
    except:
        freelancer = request.user

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

        user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email,
                                   password=password)
        user.set_password(password)
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


FORMS = [('0', LevelForm), ('1', ResumeForm), ('2', LanguageForm), ('3', EducationForm), ('4', ExperienceForm),
         ('5', BioForm), ]
TEMPLATES = {
    '0': 'users/level.html',
    '1': 'users/resume.html',
    '2': 'users/language.html',
    '3': 'users/education.html',
    '4': 'users/experience.html',
    '5': 'users/biography.html',
}


class FreelanceLogin(LoginRequiredMixin, SessionWizardView):
    template_name = 'users/wizard.html'
    success_url = reverse_lazy('index')
    form_list = FORMS
    file_storage = MyStorage()

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        organization = form_list[4].cleaned_data['organization']
        post = form_list[4].cleaned_data['post']
        month = form_list[4].cleaned_data['start_work_month']
        year = form_list[4].cleaned_data['start_work_year']
        user = self.request.user.profile.freelancer
        level_education = form_list[3].cleaned_data['level']
        institution = form_list[3].cleaned_data['institution']
        level_language = form_list[2].cleaned_data['level']
        if level_language:
            language = Language.objects.create(
                owner=user,
                level=form_list[2].cleaned_data['level'],
                language=form_list[2].cleaned_data['language']
            )
            language.save()
        if level_education and institution:
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
        if organization and post and month and year:
            experience = Experience.objects.create(
                owner=user,
                organization=organization,
                post=post,
                duties=form_list[4].cleaned_data['duties'],
                work_here=form_list[4].cleaned_data['work_here']
            )
            experience.save()
            start_work = StartWork(
                work=experience,
                month=month[0],
                year=year
            )
            start_work.save()
            if experience.work_here == False:
                end_work = EndWork(
                    work=experience,
                    month=form_list[4].cleaned_data['end_work_month'],
                    year=form_list[4].cleaned_data['end_work_year']
                )
                end_work.save()
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


@login_required(login_url='login')
def serves_add(request):
    user = request.user.profile.freelancer
    if request.method == 'POST':
        serves = request.POST.getlist('service')
        user.serves.set(serves)
        return redirect('talent_add')
    context = {'service': Services.objects.all()}
    return render(request, 'users/serves_add.html', context)


@login_required(login_url='login')
def profile_update(request):
    profile = request.user.profile

    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():

            form.save()
            return redirect('index')
        else:
            messages.error(request, form.errors)
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    feedbacks = profile.owner.all()
    try:
        s = profile.freelancer.talent_set.all()[0].id
        if request.GET.get('s'):
            s = request.GET.get('s')
        talent = Talent.objects.get(id=s)

        role = profile.freelancer

        context = {'profile': profile, 'role': role, 'talent': talent, 'feedbacks':feedbacks}
        return render(request, 'users/profile.html', context)
    except:
        context = {'profile': profile, 'feedbacks': feedbacks}
        return render(request, 'users/profile.html', context)


def all_messages(request):
    user = request.user.profile
    grouped_messages = (Message.objects
                        .filter(Q(sender=user) | Q(recipient=user))
                        .annotate(
        other_user=Case(
            When(sender=user, then=F('recipient')),
            default=F('sender'),
            output_field=IntegerField()
        )
    )
                        .values('other_user')
                        .annotate(
        pk=Max('pk')
    )
                        .values('other_user', 'pk')
                        .order_by('other_user')
                        )
    print(grouped_messages)
    send_messages = Message.objects.filter(pk__in=[msg['pk'] for msg in grouped_messages]).order_by('is_read').order_by(
        '-created')
    received_messages = Message.objects.filter(recipient=user)
    unread_count = received_messages.filter(is_read=False).count()

    context = {
        'send_messages': send_messages,
        'unread_count': unread_count,
        'received_messages': received_messages,
    }

    return render(request, 'users/all_messages.html', context)


def chat(request, pk):
    user = request.user.profile
    interlocutor = Profile.objects.get(id=pk)
    conversation = Message.objects.filter(
        (Q(sender=user) & Q(recipient=interlocutor)) | (Q(sender=interlocutor) & Q(recipient=user))).order_by(
        'is_read').order_by('created')
    messages = Message.objects.filter((Q(sender=interlocutor) & Q(recipient=user)))
    for msg in messages:
        if msg.is_read is False:
            msg.is_read = True
            msg.save()
    context = {
        'conversation': conversation, 'id': pk
    }
    if request.method == 'POST':
        msg = request.POST.get('msg')
        new_msg = Message(
            sender=user,
            recipient=interlocutor,
            body=msg
        )
        new_msg.save()
        return render(request, 'users/chat.html', context)
    return render(request, 'users/chat.html', context)


def leave_review(request, pk):
    user = request.user.profile
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        if rating and text:
            feedback = Feedback(
                owner=profile,
                sender=user,
                rating=rating,
                body=text
            )
            feedback.save()
        return redirect(request.POST.get('return_url'))
    return redirect(request.POST.get('return_url'))
