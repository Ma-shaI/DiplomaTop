from django.shortcuts import render, redirect
from .forms import *
from .models import *
from formtools.wizard.views import SessionWizardView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .utils import search_tasks


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
            return redirect('my_tasks')

    return render(request, 'tasks/task_budget_form.html', context)


def find_work(request):
    tasks, search_query = search_tasks(request)
    context = {'tasks': tasks, 'search_query': search_query}
    if request.GET.get('save'):
        profile = request.user.profile
        tasks = Task.objects.filter(freelancer_saved__owner=profile)
        context = {'tasks': tasks}
        return render(request, 'tasks/find_work.html', context)
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

            response_data = {'result': 'success'}
            return JsonResponse(response_data)

    return render(request, 'tasks/find_work.html', context)


@login_required(login_url='login')
def like_task(request):
    profile = request.user.profile
    tasks = Task.objects.filter(freelancer_saved__owner=profile)
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
        return render(request, 'tasks/saved_tasks.html', context)

    return render(request, 'tasks/like_task.html', context)


def task(request, pk):
    job = Task.objects.get(id=pk)
    customer = job.owner
    tasks = Task.objects.filter(owner=customer).filter(is_published=True)
    feedbacks = customer.owner.owner.all()
    context = {'task': job, 'customer': customer, 'tasks': tasks, 'feedbacks': feedbacks}
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        if task_id:
            task = Task.objects.get(id=task_id)
            task.freelancer_responded.add(request.user.profile.freelancer)
            task.save()
        return render(request, 'tasks/task.html', context, )
    return render(request, 'tasks/task.html', context)


def saved_tasks(request):
    profile = request.user.profile
    tasks = Task.objects.filter(freelancer_saved__owner=profile)
    context = {'tasks': tasks}
    return render(request, 'tasks/saved_tasks.html', context)


def my_offers(request):
    user = request.user.profile.freelancer
    offers = Offers.objects.filter(prospective_employee=user)
    context = {'offers': offers}
    return render(request, 'tasks/offers_page.html', context)


def my_tasks(request):
    profile = request.user.profile.customer
    task_in = Task.objects.filter(owner=profile)
    tasks = task_in.exclude(offers__isnull=False)
    contex = {'tasks': tasks}
    return render(request, 'tasks/my_tasks.html', contex)


def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('my_tasks')


def update_task(request, pk):
    profile = request.user.profile.customer
    task = profile.tasks.get(id=pk)
    budget = task.budget_set.get(owner=task)
    form_task = TaskForm(instance=task)
    form_budget = BudgetForm(instance=budget)
    context = {'task': task, 'form_task': form_task, 'form_budget': form_budget}

    if request.method == 'POST':
        currency = ''
        if request.POST['select_min_price'] == request.POST['select_max_price']:
            currency = request.POST['select_min_price']
        else:
            messages.error(request, 'Валюта должна быть одинаковой')
            return render(request, 'tasks/update_task.html', context)
        form_task = TaskForm(request.POST, instance=task)
        form_budget = BudgetForm(request.POST, instance=budget)

        if form_task.is_valid() and form_budget.is_valid():
            form_task.save()
            budget = form_budget.save(commit=False)
            budget.owner = task
            if budget.name == 'hourly_rate':
                budget.currency = currency
            else:
                budget.currency = request.POST['select_fix_price']
            budget.save()
            return redirect('my_tasks')

    return render(request, 'tasks/update_task.html', context)


def send_offer(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        freelancer_id = request.POST.get('freelancer_id')
        print(task_id)
        print(freelancer_id)
        if task_id and freelancer_id:
            freelancer = Freelancer.objects.get(id=freelancer_id)
            task = Task.objects.get(id=task_id)
            offer = Offers(
                task=task,
                prospective_employee=freelancer
            )
            offer.save()
        return redirect(request.POST.get('return_url'))
    return redirect(request.POST.get('return_url'))


def accept_offer(request, pk):
    user = request.user.profile.freelancer
    offer = Offers.objects.get(id=pk)
    if request.method == 'POST':
        answer = request.POST.get('accept')
        if answer == 'true':
            offer.at_work = True
            offer.save
            work = Work(
                work=offer.task,
                worker=user
            )
            work.save()
        elif answer == 'false':
            offer.delete()
    return redirect('offers')
