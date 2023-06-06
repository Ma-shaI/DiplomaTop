# Generated by Django 4.2.1 on 2023-06-06 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_language_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='end_work',
        ),
        migrations.RemoveField(
            model_name='experience',
            name='start_work',
        ),
        migrations.AddField(
            model_name='experience',
            name='work_here',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='StartWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('January,', 'Январь'), ('February', 'Февраль'), ('March', 'Март'), ('April', 'Апрель'), ('May', 'Май'), ('June', 'Июнь'), ('July', 'Июль'), ('August', 'Август'), ('September', 'Сентябрь'), ('October', 'Октябрь'), ('November', 'Ноябрь'), ('December', 'Декабрь')], max_length=200)),
                ('year', models.IntegerField()),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.experience')),
            ],
        ),
        migrations.CreateModel(
            name='EndWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('January,', 'Январь'), ('February', 'Февраль'), ('March', 'Март'), ('April', 'Апрель'), ('May', 'Май'), ('June', 'Июнь'), ('July', 'Июль'), ('August', 'Август'), ('September', 'Сентябрь'), ('October', 'Октябрь'), ('November', 'Ноябрь'), ('December', 'Декабрь')], max_length=200)),
                ('year', models.IntegerField()),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.experience')),
            ],
        ),
    ]
