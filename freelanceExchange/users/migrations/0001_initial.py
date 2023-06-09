# Generated by Django 4.2.1 on 2023-06-01 06:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Freelancer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiences_for_freelance', models.CharField(blank=True, choices=[('junior', 'Я новичок'), ('middle', 'У меня есть некоторый опыт'), ('senior', 'Я эксперт')], max_length=200, null=True)),
                ('resume', models.FileField(blank=True, upload_to='freelancers/resumes/%Y/%m/%d/')),
                ('bio', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='users.services')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(max_length=500, unique=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('photo', models.ImageField(default='default.jpg', upload_to='users/%Y/%m/%d/')),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('second_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('role', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, choices=[('aba', 'Абазинский'), ('abk', 'Абхазский'), ('ava', 'Аварский'), ('aze', 'Азербайджанский'), ('alb', 'Албанский'), ('amh', 'Амхарский'), ('eng', 'Английский'), ('arm', 'Армянский'), ('afr', 'Африкаанс'), ('baq', 'Баскский'), ('bak', 'Башкирский'), ('bel', 'Белорусский'), ('ben', 'Бенгальский'), ('bur', 'Бирманский'), ('bul', 'Болгарский'), ('bua', 'Бурятский'), ('hun', 'Венгерский'), ('vie', 'Вьетнамский'), ('geo', 'Грузинский'), ('dag', 'Даргинский'), ('dan', 'Датский'), ('heb', 'Иврит'), ('ind', 'Индонезийский'), ('gai', 'Ирландский'), ('ice', 'Исландский'), ('esl', 'Испанский'), ('ita', 'Итальянский'), ('kad', 'Кабардино-черкесский'), ('kaz', 'Казахский'), ('kah', 'Карачаево-балкарский'), ('kae', 'Карельский'), ('cat', 'Каталанский'), ('chi', 'Китайский'), ('kom', 'Коми'), ('kor', 'Корейский'), ('kur', 'Курдский'), ('kyr', 'Киргизский'), ('lak', 'Лакский'), ('lao', 'Лаосский'), ('lat', 'Латинский'), ('lav', 'Латышский'), ('lez', 'Лезгинский'), ('lit', 'Литовский'), ('mac', 'Македонский'), ('vog', 'Мансийский'), ('chm', 'Марийский'), ('mol', 'Молдавский'), ('mon', 'Монгольский'), ('deu', 'Немецкий'), ('nep', 'Непальский'), ('nog', 'Ногайский'), ('nor', 'Норвежский'), ('oss', 'Осетинский'), ('pan', 'Пенджабский'), ('fas', 'Персидский'), ('роr', 'Португальский'), ('pus', 'Пушту'), ('ron', 'Румынский'), ('rus', 'Русский'), ('san', 'Санскрит'), ('srp', 'Сербский'), ('slk', 'Словацкий'), ('slv', 'Словенский'), ('som', 'Сомали'), ('swa', 'Суахили'), ('tgl', 'Тагальский'), ('tgk', 'Таджикский'), ('tha', 'Тайский'), ('tam', 'Тамильский'), ('tat', 'Татарский'), ('bod', 'Тибетский'), ('tyv', 'Тувинский'), ('tur', 'Турецкий'), ('tuk', 'Туркменский'), ('vot', 'Удмуртский'), ('uzb', 'Узбекский'), ('uig', 'Уйгурский'), ('ukr', 'Украинский'), ('urd', 'Урду'), ('fin', 'Финский'), ('fra', 'Французский'), ('hin', 'Хинди'), ('hrv', 'Хорватский'), ('che', 'Чеченский'), ('ces', 'Чешский'), ('chv', 'Чувашский'), ('epo', 'Эсперанто'), ('est', 'Эстонский'), ('sah', 'Якутский'), ('jpn', 'Японский')], max_length=200, null=True)),
                ('level', models.CharField(blank=True, choices=[('A1', 'Начальный'), ('A2', 'Элементарный'), ('B1', 'Средний'), ('B2', 'Средне-продвинутый'), ('C1', 'Продвинутый'), ('C2', 'В совершенстве')], max_length=200, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.freelancer')),
            ],
        ),
        migrations.AddField(
            model_name='freelancer',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='serves',
            field=models.ManyToManyField(blank=True, to='users.services'),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=250)),
                ('post', models.CharField(max_length=250)),
                ('duties', models.TextField(blank=True, null=True)),
                ('start_work', models.IntegerField(null=True)),
                ('end_work', models.IntegerField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.freelancer')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(blank=True, choices=[('secondary', 'Среднее'), ('special_secondary', 'Среднее специальное'), ('unfinished_higher', 'Неоконченное высшее'), ('higher', 'Высшее'), ('bachelor', 'Бакалавр'), ('master', 'Магистр'), ('candidate', 'Кандидат наук'), ('doctor', 'Доктор наук')], max_length=200, null=True)),
                ('institution', models.CharField(blank=True, max_length=500, null=True)),
                ('faculty', models.CharField(blank=True, max_length=500, null=True)),
                ('major', models.CharField(blank=True, max_length=500, null=True)),
                ('start_training', models.IntegerField(null=True)),
                ('end_training', models.IntegerField(null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.freelancer')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
