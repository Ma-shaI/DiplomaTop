from django.db import models
from users.models import Customer, Freelancer
from talents.models import Skills

CURRENCY = (
    ('ruble', '₽'),
    ('dollar', '$'),
    ('euro', '€')
)


class Budget(models.Model):
    NAME = (('hourly_rate', 'Почасовая ставка'), ('fix', 'Фиксированная цена'))
    owner = models.ForeignKey('Task', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, choices=NAME)
    min_price = models.IntegerField(null=True, blank=True)
    max_price = models.IntegerField(null=True, blank=True)
    fix_price = models.IntegerField(null=True, blank=True)
    currency = models.CharField(choices=CURRENCY, default='ruble', max_length=200)

    def __str__(self):
        return f'{self.owner.title}'


class Task(models.Model):
    EXPERIENCE = (
        ('junior', 'Начальный уровень'),
        ('middle', 'Средний уровень'),
        ('senior', 'Эксперт')
    )

    AMOUNT_OF_WORK = (
        ('tiny', 'Менее 1 месяца'),
        ('little', 'От 1 до 3 месяцев'),
        ('medium', 'От 3 до 6 месяцев'),
        ('big', 'Более 6 месяцев')
    )

    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    experiences = models.CharField(max_length=200, choices=EXPERIENCE, verbose_name='Уровень опыта')
    amount_of_work = models.CharField(max_length=200, choices=AMOUNT_OF_WORK, verbose_name='Объем работы')
    contract_work = models.BooleanField(verbose_name='Работа по контракту')
    description = models.TextField(verbose_name='Описание')
    skills = models.ManyToManyField(Skills, blank=True, verbose_name='Навыки')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовать')
    freelancer_saved = models.ManyToManyField(Freelancer, blank=True, related_name='saved_tasks')
    freelancer_responded = models.ManyToManyField(Freelancer, blank=True, related_name='responded_tasks')

    def __str__(self):
        return f'{self.title}'


class Work(models.Model):
    work = models.OneToOneField(Task, on_delete=models.CASCADE)
    worker = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='worker')
    created = models.DateTimeField(auto_now_add=True)
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.work}'


class StagesOfWork(models.Model):
    owner = models.ForeignKey(Work, on_delete=models.CASCADE)
    stage = models.TextField()
    done = models.BooleanField(default=False)
    max_term = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.stage}'


class Offers(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    prospective_employee = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='prospective_employee')
    request_date = models.DateTimeField(auto_now_add=True)
    at_work = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task}'
