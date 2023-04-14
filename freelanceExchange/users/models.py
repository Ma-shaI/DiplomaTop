from django.db import models
from django.contrib.auth.models import User


class Experience(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class LevelsEducation(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class LevelsLanguage(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500)
    username = models.CharField(max_length=200, null=True, blank=True)
    experiences = models.ManyToManyField(Experience, blank=True)
    resume = models.FileField(upload_to='freelancers/resumes/%Y/%m/%d/', blank=True)
    profile_image = models.ImageField(upload_to='freelancers/', default='user-default.png')
    bio = models.TextField(null=True, blank=True)
    hourly_rate = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.first_name}'


class Education(models.Model):
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE, null=True, blank=True)
    level = models.ManyToManyField(LevelsEducation, blank=True)
    institution = models.CharField(max_length=500, blank=True, null=True)
    faculty = models.CharField(max_length=500, blank=True, null=True)
    major = models.CharField(max_length=500, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.major}'


class Languages(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    level = models.ManyToManyField(LevelsLanguage, blank=True)

    def __str__(self):
        return f'{self.name}'


class Skill(models.Model):
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
