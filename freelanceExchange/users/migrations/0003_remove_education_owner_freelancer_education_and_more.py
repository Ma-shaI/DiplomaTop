# Generated by Django 4.1.7 on 2023-04-20 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='owner',
        ),
        migrations.AddField(
            model_name='freelancer',
            name='education',
            field=models.ManyToManyField(blank=True, null=True, to='users.education'),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='language',
            field=models.ManyToManyField(blank=True, null=True, to='users.languages'),
        ),
    ]