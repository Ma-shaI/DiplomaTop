from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from .utils import LEVEL, LANGUAGE, MONTH


class Role(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', default='default.jpg')
    country = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    second_number = PhoneNumberField(null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}'


class Services(MPTTModel):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name}'


class Education(models.Model):
    LEVEL = (('secondary', 'Среднее'),
             ('special_secondary', 'Среднее специальное'),
             ('unfinished_higher', 'Неоконченное высшее'),
             ('higher', 'Высшее'),
             ('bachelor', 'Бакалавр'),
             ('master', 'Магистр'),
             ('candidate', 'Кандидат наук'),
             ('doctor', 'Доктор наук'),)
    owner = models.ForeignKey("Freelancer", on_delete=models.CASCADE, null=True, blank=True)
    level = models.CharField(choices=LEVEL, max_length=200, null=True, blank=True)
    institution = models.CharField(max_length=500, blank=True, null=True)
    faculty = models.CharField(max_length=500, blank=True, null=True)
    major = models.CharField(max_length=500, blank=True, null=True)
    start_training = models.IntegerField(null=True)
    end_training = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.major}'


class Freelancer(models.Model):
    EXPERIENCE = (
        ('junior', 'Я новичок'),
        ('middle', 'У меня есть некоторый опыт'),
        ('senior', 'Я эксперт')
    )
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE)
    experiences_for_freelance = models.CharField(max_length=200, choices=EXPERIENCE, blank=True, null=True)
    resume = models.FileField(upload_to='freelancers/resumes/%Y/%m/%d/', blank=True)
    bio = models.TextField(null=True, blank=True)
    serves = models.ManyToManyField(Services, blank=True)

    def __str__(self):
        return f'{self.owner}'


class Experience(models.Model):
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    organization = models.CharField(max_length=250, verbose_name='Организация')
    post = models.CharField(max_length=250)
    duties = models.TextField(null=True, blank=True)
    work_here = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.post}'


class StartWork(models.Model):
    work = models.ForeignKey(Experience, on_delete=models.CASCADE)
    month = models.CharField(max_length=200, choices=MONTH)
    year = models.IntegerField()

    def __str__(self):
        return f'{self.work}'


class EndWork(models.Model):
    work = models.ForeignKey(Experience, on_delete=models.CASCADE)
    month = models.CharField(max_length=200, choices=MONTH)
    year = models.IntegerField()

    def __str__(self):
        return f'{self.work}'


class Language(models.Model):
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    language = models.CharField(max_length=200, choices=LANGUAGE, blank=True, null=True)
    level = models.CharField(max_length=200, choices=LEVEL, blank=True, null=True)

    def __str__(self):
        return self.language


class Customer(models.Model):
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return f'{self.owner}'


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='sender', null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='recipient', null=True, blank=True)
    subject = models.CharField(max_length=300, null=True, blank=True)
    body = models.TextField()
    task = models.ForeignKey('tasks.Task', on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}'

    # class Meta:
    #     ordering = ['is_read', 'created']
