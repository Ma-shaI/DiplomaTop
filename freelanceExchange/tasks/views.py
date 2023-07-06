from django.shortcuts import render, redirect
from .forms import *
from .models import *
from formtools.wizard.views import SessionWizardView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from users.models import Message
from .utils import search_tasks, paginate_tasks
import datetime


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


def publish_task(request, pk):
    task = Task.objects.get(id=pk)
    context = {
        'task': task
    }
    if request.method == 'POST':
        task.is_published = True
        task.save()
        return redirect('my_tasks')
    return render(request, 'tasks/publish_task.html', context)


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
            return redirect('publish_task', pk=task.id)
        return render(request, 'tasks/task_budget_form.html', context)

    return render(request, 'tasks/task_budget_form.html', context)


def find_work(request):
    tasks, search_query = search_tasks(request)
    tasks, custom_range = paginate_tasks(request, tasks, 5)
    context = {'tasks': tasks, 'search_query': search_query, 'custom_range': custom_range}
    if request.GET.get('save'):
        profile = request.user.profile
        tasks = Task.objects.filter(freelancer_saved__owner=profile)
        context = {'tasks': tasks}
        return render(request, 'tasks/find_work.html', context)

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
            message = Message.objects.create(
                sender=request.user.profile,
                recipient=task.owner.owner,
                subject='response to a vacancy',
                body=f'Добрый день, мне интересна ваша вакансия.',
            )
            message.save()
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
            offer.save()
            work = Work(
                work=offer.task,
                worker=user
            )
            work.save()
            return redirect('offers')
        elif answer == 'false':
            offer.delete()
            return redirect('offers')
    return redirect('offers')


def my_staff(request):
    try:
        user = request.user.profile.customer
        staff = Work.objects.filter(work__owner=user)
        content = {
            'staff': staff
        }
        return render(request, 'tasks/my_staff.html', content)
    except:
        user = request.user.profile.freelancer
        works = Work.objects.filter(worker=user)
        print(works)
        content = {
            'works': works
        }
        return render(request, 'tasks/my_works.html', content)


def work(request, pk):
    work = Work.objects.get(id=pk)
    stages = StagesOfWork.objects.filter(owner=work)
    context = {
        'work': work,
        'stages': stages,
    }

    return render(request, 'tasks/work.html', context)


def add_stage(request):
    if request.method == 'POST':
        new_stage = request.POST.get('stage')
        max_term = request.POST.get('max-term')
        work_id = request.POST.get('work')
        if new_stage and max_term and work_id:
            work = Work.objects.get(id=work_id)
            stage = StagesOfWork(
                owner=work,
                stage=new_stage,
                max_term=max_term
            )
            stage.save()
            return redirect(request.POST.get('return_url'))
    return redirect(request.POST.get('return_url'))


def done_stage(request, pk):
    if request.method == 'POST':
        stage_id = request.POST.get('task_id')
        now = datetime.datetime.now()
        if stage_id:
            stage = StagesOfWork.objects.get(id=stage_id)
            stage.done = not stage.done

            stage.save()
            if stage.done == True:
                stage.update_time = now
                stage.save()
        return redirect(request.POST.get('return_url'))
    return redirect(request.POST.get('return_url'))


def responded_task(request):
    user = request.user.profile.customer
    tasks = Task.objects.filter(owner=user)
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/responded.html', context)
