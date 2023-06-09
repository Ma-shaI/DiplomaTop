from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from talents.forms import TalentForm
from .forms import *
from .models import *
from formtools.wizard.views import SessionWizardView
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from talents.models import *
from django.db.models import Q
from django.db.models import Max, Count, Case, When, F, Value, CharField, IntegerField
from tasks.models import Task
from .utils import paginate_feedbacks, get_common_context
from django.db.models import Avg
from base.utils import get_messages, paginate_data


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
        password1 = form_list[1].cleaned_data['password1']
        password2 = form_list[1].cleaned_data['password2']
        if password1 == password2:
            password = password1

            if User.objects.filter(username=username).exists():
                messages.error(self.request, 'Пользователь с такой почтой уже существует')
                return self.render_goto_step(0)
            else:
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
        messages.error(self.request, 'Пароли должны совпадать')
        return self.render_goto_step(0)


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
    if feedbacks:
        average_rating = round((feedbacks.aggregate(Avg('rating'))['rating__avg']), 2)
    else:
        average_rating = ''
    feedbacks, custom_range = paginate_feedbacks(request, feedbacks, 3)
    try:
        talents = profile.freelancer.talent_set.all() if hasattr(profile,
                                                                 'freelancer') else profile.customer.tasks.all()
        s = talents[0].id
        if request.GET.get('s'):
            s = request.GET.get('s')
        talent = Talent.objects.get(id=s) if hasattr(profile, 'freelancer') else Task.objects.get(id=s)
    except:
        talents = ''
        talent = ''
    form = TalentForm() if hasattr(profile, 'freelancer') else None
    freelancer = profile.freelancer if hasattr(profile, 'freelancer') else None
    try:
        tasks = Task.objects.filter(owner=request.user.profile.customer).filter(is_published=True)
    except:
        tasks = ''
    context = get_common_context(profile, feedbacks, custom_range, average_rating, talents, talent, freelancer,
                                 tasks, form)
    context.update(get_messages(request.user.profile))
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
    send_messages = Message.objects.filter(pk__in=[msg['pk'] for msg in grouped_messages]).order_by('is_read').order_by(
        '-created')
    send_messages, custom_range = paginate_data(request, send_messages, 10)
    context = {'send_messages': send_messages, 'custom_range': custom_range}
    context.update(get_messages(request.user.profile))
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
        'conversation': conversation, 'id': pk, 'interlocutor': interlocutor
    }
    context.update(get_messages(request.user.profile))
    if request.method == 'POST':
        msg = request.POST.get('msg')
        if msg:
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
        if rating:
            feedback = Feedback(
                owner=profile,
                sender=user,
                rating=rating,
                body=text
            )
            feedback.save()
        return redirect(request.POST.get('return_url'))
    return redirect(request.POST.get('return_url'))


def language_add(request):
    form = LanguageForm()
    user = request.user.profile
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = request.POST.get('2-language')
            level = request.POST.get('2-level')
            language_add = Language(
                owner=user,
                language=language,
                level=level
            )
            language_add.save()
            return redirect(request.POST.get('return_url'))
    context = {
        'form': form
    }
    return redirect(request, 'users/language.html', context)
