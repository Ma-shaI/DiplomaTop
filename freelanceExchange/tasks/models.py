from django.db import models
from users.models import Customer, Freelancer
from talents.models import Skills
from talents.utils import CURRENCY


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

    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    experiences = models.CharField(max_length=200, choices=EXPERIENCE)
    amount_of_work = models.CharField(max_length=200, choices=AMOUNT_OF_WORK)
    contract_work = models.BooleanField()
    description = models.TextField()
    skills = models.ManyToManyField(Skills, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    freelancer_saved = models.ManyToManyField(Freelancer, blank=True)

    def __str__(self):
        return f'{self.title}'
