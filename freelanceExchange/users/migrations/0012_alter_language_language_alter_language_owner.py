# Generated by Django 4.2.1 on 2023-07-07 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_feedback_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='language',
            field=models.CharField(blank=True, choices=[('', ''), ('aba', 'Абазинский'), ('abk', 'Абхазский'), ('ava', 'Аварский'), ('aze', 'Азербайджанский'), ('alb', 'Албанский'), ('amh', 'Амхарский'), ('eng', 'Английский'), ('arm', 'Армянский'), ('afr', 'Африкаанс'), ('baq', 'Баскский'), ('bak', 'Башкирский'), ('bel', 'Белорусский'), ('ben', 'Бенгальский'), ('bur', 'Бирманский'), ('bul', 'Болгарский'), ('bua', 'Бурятский'), ('hun', 'Венгерский'), ('vie', 'Вьетнамский'), ('geo', 'Грузинский'), ('dag', 'Даргинский'), ('dan', 'Датский'), ('heb', 'Иврит'), ('ind', 'Индонезийский'), ('gai', 'Ирландский'), ('ice', 'Исландский'), ('esl', 'Испанский'), ('ita', 'Итальянский'), ('kad', 'Кабардино-черкесский'), ('kaz', 'Казахский'), ('kah', 'Карачаево-балкарский'), ('kae', 'Карельский'), ('cat', 'Каталанский'), ('chi', 'Китайский'), ('kom', 'Коми'), ('kor', 'Корейский'), ('kur', 'Курдский'), ('kyr', 'Киргизский'), ('lak', 'Лакский'), ('lao', 'Лаосский'), ('lat', 'Латинский'), ('lav', 'Латышский'), ('lez', 'Лезгинский'), ('lit', 'Литовский'), ('mac', 'Македонский'), ('vog', 'Мансийский'), ('chm', 'Марийский'), ('mol', 'Молдавский'), ('mon', 'Монгольский'), ('deu', 'Немецкий'), ('nep', 'Непальский'), ('nog', 'Ногайский'), ('nor', 'Норвежский'), ('oss', 'Осетинский'), ('pan', 'Пенджабский'), ('fas', 'Персидский'), ('роr', 'Португальский'), ('pus', 'Пушту'), ('ron', 'Румынский'), ('rus', 'Русский'), ('san', 'Санскрит'), ('srp', 'Сербский'), ('slk', 'Словацкий'), ('slv', 'Словенский'), ('som', 'Сомали'), ('swa', 'Суахили'), ('tgl', 'Тагальский'), ('tgk', 'Таджикский'), ('tha', 'Тайский'), ('tam', 'Тамильский'), ('tat', 'Татарский'), ('bod', 'Тибетский'), ('tyv', 'Тувинский'), ('tur', 'Турецкий'), ('tuk', 'Туркменский'), ('vot', 'Удмуртский'), ('uzb', 'Узбекский'), ('uig', 'Уйгурский'), ('ukr', 'Украинский'), ('urd', 'Урду'), ('fin', 'Финский'), ('fra', 'Французский'), ('hin', 'Хинди'), ('hrv', 'Хорватский'), ('che', 'Чеченский'), ('ces', 'Чешский'), ('chv', 'Чувашский'), ('epo', 'Эсперанто'), ('est', 'Эстонский'), ('sah', 'Якутский'), ('jpn', 'Японский')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
