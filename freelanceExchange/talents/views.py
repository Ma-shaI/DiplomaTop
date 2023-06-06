from django.shortcuts import render, redirect
from .forms import *


def talent_add(request):
    form = TalentForm()
    user = request.user.profile.freelancer
    if request.method == 'POST':
        new_skills = request.POST.get('new_skills').replace(',', ' ').split()
       
        form = TalentForm(request.POST)

        if form.is_valid():
            for skill in new_skills:

                skill, created = Skills.objects.get_or_create(title=skill)
            talent = form.save(commit=False)
            talent.owner = user
            talent.save()
        return redirect('profile_update')
    context = {'form': form}
    return render(request, 'talents/talent_add.html', context)
