from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField


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
    secondPhoneNumber = PhoneNumberField(null=True, blank=True)
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


class LevelsEducation(models.Model):
    name = models.CharField(max_length=200)

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
    EXPERIENCE = (
        ('junior', 'Я новичок'),
        ('middle', 'У меня есть некоторый опыт'),
        ('senior', 'Я эксперт')
    )
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE)
    experiences_for_freelance = models.CharField(max_length=200, choices=EXPERIENCE, blank=True, null=True)
    resume = models.FileField(upload_to='freelancers/resumes/%Y/%m/%d/', blank=True)
    education = models.ManyToManyField(Education, blank=True)
    bio = models.TextField(null=True, blank=True)
    serves = models.ManyToManyField(Services, blank=True)

    def __str__(self):
        return f'{self.owner}'


class Experience(models.Model):
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    organization = models.CharField(max_length=250)
    post = models.CharField(max_length=250)
    duties = models.TextField(null=True, blank=True)
    start_work = models.DateTimeField(null=True)
    end_work = models.DateTimeField(null=True)


class Language(models.Model):
    LEVEL = (
        ('A1', 'Начальный'),
        ('A2', 'Элементарный'),
        ('B1', 'Средний'),
        ('B2', 'Средне-продвинутый'),
        ('C1', 'Продвинутый'),
        ('C2', 'В совершенстве')
    )
    LANGUAGE = (
        ('aba', 'Абазинский'),
        ('abk', 'Абхазский'),
        ('ava', 'Аварский'),
        ('aze', 'Азербайджанский'),
        ('alb', 'Албанский'),
        ('amh', 'Амхарский'),
        ('eng', 'Английский'),
        ('arm', 'Армянский'),
        ('afr', 'Африкаанс'),
        ('baq', 'Баскский'),
        ('bak', 'Башкирский'),
        ('bel', 'Белорусский'),
        ('ben', 'Бенгальский'),
        ('bur', 'Бирманский'),
        ('bul', 'Болгарский'),
        ('bua', 'Бурятский'),
        ('hun', 'Венгерский'),
        ('vie', 'Вьетнамский'),
        ('geo', 'Грузинский'),
        ('dag', 'Даргинский'),
        ('dan', 'Датский'),
        ('heb', 'Иврит'),
        ('ind', 'Индонезийский'),
        ('gai', 'Ирландский'),
        ('ice', 'Исландский'),
        ('esl', 'Испанский'),
        ('ita', 'Итальянский'),
        ('kad', 'Кабардино-черкесский'),
        ('kaz', 'Казахский'),
        ('kah', 'Карачаево-балкарский'),
        ('kae', 'Карельский'),
        ('cat', 'Каталанский'),
        ('chi', 'Китайский'),
        ('kom', 'Коми'),
        ('kor', 'Корейский'),
        ('kur', 'Курдский'),
        ('kyr', 'Киргизский'),
        ('lak', 'Лакский'),
        ('lao', 'Лаосский'),
        ('lat', 'Латинский'),
        ('lav', 'Латышский'),
        ('lez', 'Лезгинский'),
        ('lit', 'Литовский'),
        ('mac', 'Македонский'),
        ('vog', 'Мансийский'),
        ('chm', 'Марийский'),
        ('mol', 'Молдавский'),
        ('mon', 'Монгольский'),
        ('deu', 'Немецкий'),
        ('nep', 'Непальский'),
        ('nog', 'Ногайский'),
        ('nor', 'Норвежский'),
        ('oss', 'Осетинский'),
        ('pan', 'Пенджабский'),
        ('fas', 'Персидский'),
        ('роr', 'Португальский'),
        ('pus', 'Пушту'),
        ('ron', 'Румынский'),
        ('rus', 'Русский'),
        ('san', 'Санскрит'),
        ('srp', 'Сербский'),
        ('slk', 'Словацкий'),
        ('slv', 'Словенский'),
        ('som', 'Сомали'),
        ('swa', 'Суахили'),
        ('tgl', 'Тагальский'),
        ('tgk', 'Таджикский'),
        ('tha', 'Тайский'),
        ('tam', 'Тамильский'),
        ('tat', 'Татарский'),
        ('bod', 'Тибетский'),
        ('tyv', 'Тувинский'),
        ('tur', 'Турецкий'),
        ('tuk', 'Туркменский'),
        ('vot', 'Удмуртский'),
        ('uzb', 'Узбекский'),
        ('uig', 'Уйгурский'),
        ('ukr', 'Украинский'),
        ('urd', 'Урду'),
        ('fin', 'Финский'),
        ('fra', 'Французский'),
        ('hin', 'Хинди'),
        ('hrv', 'Хорватский'),
        ('che', 'Чеченский'),
        ('ces', 'Чешский'),
        ('chv', 'Чувашский'),
        ('epo', 'Эсперанто'),
        ('est', 'Эстонский'),
        ('sah', 'Якутский'),
        ('jpn', 'Японский'))
    owner = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    language = models.CharField(max_length=200, choices=LANGUAGE, blank=True, null=True)
    level = models.CharField(max_length=200, choices=LEVEL, blank=True, null=True)

    def __str__(self):
        return self.language


class Customer(models.Model):
    owner = models.OneToOneField(Profile, on_delete=models.CASCADE)
