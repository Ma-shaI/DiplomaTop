from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError


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
        print(new_skills)
        if talent_form.is_valid() and rate_form.is_valid():
            talent_form.save()

            for skill in new_skills:
                skill, created = Skills.objects.get_or_create(title=skill)
                talent.skills.add(skill.id)

            rate_form.save()
            return redirect('index')

    context = {'talent_form': talent_form, 'rate_form': rate_form, 'talent': talent, 'skills': talent.skills.all()}

    return render(request, 'talents/talent_update.html', context)


def talent_delete(request, pk):
    user = request.user.profile.freelancer
    talent = user.talent_set.get(id=pk)
    talent.delete()
    return redirect('talent_add')


def liked_talent(request, pk):
    profile = request.user.profile
    talents = Talent.objects.filter(customer_saved__owner=profile)
    context = {'talents': talents}
    if request.method == 'POST':
        talent_id = request.POST.get('task_id')

        if talent_id:
            talent = Talent.objects.get(id=talent_id)
            if request.user.profile.customer in talent.customer_saved.all():

                talent.customer_saved.remove(profile.customer)
                talent.save()
            else:

                talent.customer_saved.add(profile.customer)
                talent.save()
        return render(request, 'talents/find_talent.html', context)
    return render(request, 'talents/liked_talent.html', context)


def find_talent(request):
    talents = Talent.objects.all()
    context = {'talents': talents}
    if request.method == 'POST':
        talent_id = request.POST.get('talent_id')
        if talent_id:
            talent = Talent.objects.get(id=talent_id)
            talent.customer_invited.add(request.user.profile.customer)
            talent.save()
        return render(request, 'talents/find_talent.html', context)
    return render(request, 'talents/find_talent.html', context)
