from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Services(MPTTModel):
    name = models.CharField(max_length=200, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name}'


class Experience(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class LevelsEducation(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'



class Languages(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Education(models.Model):
    level = models.ManyToManyField(LevelsEducation, blank=True)
    institution = models.CharField(max_length=500, blank=True, null=True)
    faculty = models.CharField(max_length=500, blank=True, null=True)
    major = models.CharField(max_length=500, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.major}'


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
    serves = models.ManyToManyField(Services)

    def __str__(self):
        return f'{self.first_name}'


class Skill(models.Model):
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500)
    username = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}'


class Language(models.Model):
    LEVEL = (
        ('A1', 'Начальный'),
        ('A2', 'Элементарный'),
        ('B1', 'Средний'),
        ('B2', 'Средне-продвинутый'),
        ('C1', 'Продвинутый'),
        ('C2', 'В совершенстве')
    )
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    language = models.ManyToManyField(Languages, blank=True)
    level = models.CharField(max_length=200, choices=LEVEL)

    def __str__(self):
        return self.language
