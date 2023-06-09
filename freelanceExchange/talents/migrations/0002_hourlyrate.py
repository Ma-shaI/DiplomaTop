# Generated by Django 4.2.1 on 2023-06-06 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourlyRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
                ('currency', models.CharField(choices=[('ruble', '₽'), ('dollar', '$'), ('euro', '€')], default='ruble', max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talents.talent')),
            ],
        ),
    ]
