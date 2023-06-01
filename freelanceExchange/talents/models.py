from django.db import models
from users.models import Freelancer, Services


class Talent(models.Model):
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=250)
    descriptions = models.TextField()
    hourly_rate = models.IntegerField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField('Skills', blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Skills(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
