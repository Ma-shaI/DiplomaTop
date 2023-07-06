from django.shortcuts import render, redirect
from .forms import *
from .models import *
from users.models import Message
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from tasks.models import Task
from .utils import search_talent, paginate_talent
from django.http import JsonResponse


@login_required(login_url='login')
def talent_add(request):
    form = TalentForm()
    user = request.user.profile.freelancer
    talents = Talent.objects.filter(owner=user)
    context = {'form': form, 'talents': talents}
    if request.method == 'POST':
        form = TalentForm(request.POST)
        if form.is_valid():
            new_skills = request.POST.get('new_skills').replace(',', ' ').split()
            title = request.POST['title']
            service = request.POST['service']
            descriptions = request.POST['descriptions']
            rate = request.POST['rate']
            currency = request.POST['currency']
            try:
                request.POST['is_published'] == 'on'
                is_published = True
            except MultiValueDictKeyError:
                is_published = False

            talent = Talent(
                owner=user,
                service=Services.objects.get(id=service),
                title=title,
                descriptions=descriptions,
                is_published=is_published
            )
            talent.save()
            for skill in new_skills:
                skill, created = Skills.objects.get_or_create(title=skill)
                talent.skills.add(skill)

            rate = HourlyRate(
                owner=talent,
                rate=rate,
                currency=currency
            )
            rate.save()
            return redirect('talent_add')

    return render(request, 'talents/talent_add.html', context)


def talent_update(request, pk):
    user = request.user.profile.freelancer
    talent = user.talent_set.get(id=pk)
    rate = HourlyRate.objects.get(owner=talent)
    talent_form = TalentUpdateForm(instance=talent)
    rate_form = RateForm(instance=rate)
    if request.method == 'POST':
        talent_form = TalentUpdateForm(request.POST, instance=talent)
        rate_form = RateForm(request.POST, instance=rate)
        new_skills = request.POST.get('new_skills').replace(',', ' ').split()

        if talent_form.is_valid() and rate_form.is_valid():
            talent_form.save()

            for skill in new_skills:
                skill, created = Skills.objects.get_or_create(title=skill)
                talent.skills.add(skill.id)

            rate_form.save()
            return redirect('profile', pk=request.user.id)

    context = {'talent_form': talent_form, 'rate_form': rate_form, 'talent': talent, 'skills': talent.skills.all()}

    return render(request, 'talents/talent_update.html', context)


def talent_delete(request, pk):
    user = request.user.profile.freelancer
    talent = user.talent_set.get(id=pk)
    talent.delete()
    return redirect('talent_add')


def like_talent(request, pk):
    profile = request.user.profile
    freelancers = Freelancer.objects.filter(customer_saved__owner=profile)
    context = {'freelancers': freelancers}
    if request.method == 'POST':
        freelancer_id = request.POST.get('task_id')

        if freelancer_id:
            freelancer = Freelancer.objects.get(id=freelancer_id)
            if request.user.profile.customer in freelancer.customer_saved.all():
                freelancer.customer_saved.remove(profile.customer)
                freelancer.save()
            else:
                freelancer.customer_saved.add(profile.customer)
                freelancer.save()
        return render(request, 'talents/find_talent.html', context)
    return render(request, 'talents/like_talent.html', context)


def find_talent(request):
    freelancers, search_query = search_talent(request)
    freelancers, custom_range = paginate_talent(request, freelancers, 3)
    tasks = Task.objects.filter(owner=request.user.profile.customer).filter(is_published=True)
    context = {'freelancers': freelancers, 'tasks': tasks, 'custom_range': custom_range}
    return render(request, 'talents/find_talent.html', context)


def saved_talents(request):
    profile = request.user.profile
    talents = Freelancer.objects.filter(customer_saved__owner=profile)
    context = {'talents': talents, 'tasks': Task.objects.filter(owner=profile.customer)}
    return render(request, 'talents/saved_talents.html', context)


def choice_task(request):
    if request.method == 'POST':
        selected_choice = request.POST.get('choice_task')
        freelancer_id = request.POST.get('talent_id')
        if freelancer_id and selected_choice:
            freelancer = Freelancer.objects.get(id=freelancer_id)
            freelancer.customer_invited.add(request.user.profile.customer)
            freelancer.save()
            message = Message.objects.create(
                sender=request.user.profile,
                recipient=freelancer.owner,
                subject='invitation to an interview',
                body=f'Приглашаю Вас на интервью, по поводу вакансии',
                task=Task.objects.get(id=selected_choice)
            )
            message.save()

        return redirect(request.POST.get('return_url'))
    return redirect(request.POST.get('return_url'))
