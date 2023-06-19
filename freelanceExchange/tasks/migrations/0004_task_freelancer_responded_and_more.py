# Generated by Django 4.2.1 on 2023-06-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_endwork_month_alter_experience_organization_and_more'),
        ('tasks', '0003_task_freelancer_saved_alter_budget_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='freelancer_responded',
            field=models.ManyToManyField(blank=True, related_name='responded_tasks', to='users.freelancer'),
        ),
        migrations.AlterField(
            model_name='task',
            name='freelancer_saved',
            field=models.ManyToManyField(blank=True, related_name='saved_tasks', to='users.freelancer'),
        ),
    ]
