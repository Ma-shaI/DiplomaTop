from django.db import models
from users.models import Freelancer, Services, Customer

CURRENCY = (
    ('ruble', '₽'),
    ('dollar', '$'),
    ('euro', '€')
)


class Talent(models.Model):
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, default=1, verbose_name='Специализация')
    title = models.CharField(max_length=250, verbose_name='Ваш заголовок')
    descriptions = models.TextField(verbose_name='Описание')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    skills = models.ManyToManyField('Skills', blank=True, verbose_name='Навыки')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовать')


    def __str__(self):
        return f"{self.title}"


class HourlyRate(models.Model):
    owner = models.ForeignKey(Talent, on_delete=models.CASCADE)
    rate = models.IntegerField(verbose_name='Почасовая ставка')
    currency = models.CharField(choices=CURRENCY, default='ruble', max_length=200, verbose_name='Валюта')

    def __str__(self):
        return f'{self.owner}'


class Skills(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.title
