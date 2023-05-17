from django.db import models
from users.models import  Customer, Experience


class AmountHours(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class AmountOfWork(models.Model):
    name = models.CharField(max_length=200)
    amount_hours = models.ManyToManyField(AmountHours)

    def __str__(self):
        return f'{self.name}'


class Budget(models.Model):
    name = models.CharField(max_length=200)
    min_price = models.IntegerField(null=True, blank=True)
    max_price = models.IntegerField(null=True, blank=True)
    fix_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Task(models.Model):
    EXPERIENCE = (
        ('junior', 'Новичок'),
        ('middle', 'Средний'),
        ('senior', 'Эксперт')
    )
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    experiences = models.CharField(max_length=200, choices=EXPERIENCE)
    amount_of_work = models.ManyToManyField(AmountOfWork, blank=True)
    contract_work = models.BooleanField()
    budget = models.ManyToManyField(Budget)
    description = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'
