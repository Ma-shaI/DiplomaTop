from django.db import models
from users.models import Freelancer, Services
from .utils import CURRENCY


class Talent(models.Model):
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=250)
    descriptions = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField('Skills', blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class HourlyRate(models.Model):
    owner = models.ForeignKey(Talent, on_delete=models.CASCADE)
    rate = models.IntegerField()
    currency = models.CharField(choices=CURRENCY, default='ruble', max_length=200)

    def __str__(self):
        return f'{self.owner}'


class Skills(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
