# Generated by Django 4.2.1 on 2023-06-07 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_experience_end_work_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='work_here',
            field=models.BooleanField(default=True),
        ),
    ]
