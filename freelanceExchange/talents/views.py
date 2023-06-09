from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError


@login_required(login_url='login')
def talent_add(request):
    form = TalentForm()
    user = request.user.profile.freelancer
    talents = Talent.objects.all()
    context = {'form': form, 'talents': talents}
    if request.method == 'POST':
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
        render(request, 'talents/talent_add.html', context)

    return render(request, 'talents/talent_add.html', context)
