# Generated by Django 4.2.1 on 2023-07-03 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_feedback_sender_alter_feedback_owner'),
        ('tasks', '0005_alter_task_amount_of_work_alter_task_contract_work_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('time_start', models.DateTimeField(blank=True, null=True)),
                ('time_end', models.DateTimeField(blank=True, null=True)),
                ('work', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker', to='users.freelancer')),
            ],
        ),
        migrations.CreateModel(
            name='StagesOfWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.TextField()),
                ('done', models.BooleanField(default=False)),
                ('max_term', models.DateTimeField()),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tasks.work')),
            ],
        ),
    ]