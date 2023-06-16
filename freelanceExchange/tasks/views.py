from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from formtools.wizard.views import SessionWizardView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


class TaskWizard(LoginRequiredMixin, SessionWizardView):
    template_name = 'tasks/task_add.html'
    done_template = 'users/index.html'
    success_url = reverse_lazy('index')
    form_list = [TaskTitleForm, TaskSkillForm, AmountOfWorkForm, DescriptionForm]

    def done(self, form_list, **kwargs):
        user = self.request.user.profile.customer
        task = Task.objects.create(
            owner=user,
            title=form_list[0].cleaned_data['title'],
            # skills=Skills.objects.get(title=form_list[1].cleaned_data['skills']),
            amount_of_work=form_list[2].cleaned_data['amount'],
            contract_work=form_list[2].cleaned_data['contract_work'],
            experiences=form_list[2].cleaned_data['experience'],
            description=form_list[3].cleaned_data['description']
        )
        task.skills.set(form_list[1].cleaned_data['skills'])
        task.save()
        return redirect('task_budget', pk=task.id)


@login_required(login_url='login')
def task_budget(request, pk):
    task = Task.objects.get(id=pk)
    form = BudgetForm()
    context = {'form': form, 'task': task}
    if request.method == 'POST':
        currency = ''
        if request.POST['select_min_price'] == request.POST['select_max_price']:
            currency = request.POST['select_min_price']
        else:
            messages.error(request, 'Валюта должна быть одинаковой')

            return render(request, 'tasks/task_budget_form.html', context)
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.owner = task
            if budget.name == 'hourly_rate':
                budget.currency = currency
            else:
                budget.currency = request.POST['select_fix_price']
            budget.save()
            return redirect('profile_update')

    return render(request, 'tasks/task_budget_form.html', context)


def find_work(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        if task_id:
            task = Task.objects.get(id=task_id)
            if request.user.profile.freelancer in task.freelancer_saved.all():
                task.freelancer_saved.remove(request.user.profile.freelancer)
                task.save()
            else:
                task.freelancer_saved.add(request.user.profile.freelancer)
                task.save()

            # Формирование ответа сервера в формате JSON
            response_data = {'result': 'success'}
            return JsonResponse(response_data)

    return render(request, 'tasks/find_work.html', context)


# def like_task(request):
#     if request.method == 'POST':
#         task_id = request.POST.get('task_id')
#         if task_id:
#             task = Task.objects.get(id=task_id)
#             if request.user.profile.freelancer in task.freelancer_saved.all():
#                 task.freelancer_saved.remove(request.user.profile.freelancer)
#                 task.save()
#             else:
#                 task.freelancer_saved.add(request.user.profile.freelancer)
#                 task.save()
#
#             # Формирование ответа сервера
#             response_data = {'success': True, 'message': 'Данные успешно обработаны'}
#             return JsonResponse(response_data)
#     return JsonResponse({'success': False, 'message': 'Ошибка: неверный метод запроса'})
