from django.core.paginator import Paginator

LEVEL = (
    ('', ''),
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

MONTH = (
    ('', 'Месяц'),
    ('January,', 'Январь'),
    ('February', 'Февраль'),
    ('March', 'Март'),
    ('April', 'Апрель'),
    ('May', 'Май'),
    ('June', 'Июнь'),
    ('July', 'Июль'),
    ('August', 'Август'),
    ('September', 'Сентябрь'),
    ('October', 'Октябрь'),
    ('November', 'Ноябрь'),
    ('December', 'Декабрь'),

)


def paginate_feedbacks(request, feedbacks, results):
    page = request.GET.get('page', 1)
    paginator = Paginator(feedbacks, results)
    feedbacks = paginator.get_page(page)
    left_index = int(page) - 4

    if left_index < 1:
        left_index = 1
    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    return feedbacks, custom_range


def get_common_context(profile, feedbacks, custom_range, average_rating, talents, talent=None, role=None,
                       freelancer=None, tasks=None, form=None):
    context = {'profile': profile, 'feedbacks': feedbacks, 'custom_range': custom_range,
               'average_rating': average_rating, 'talents': talents}
    if role:
        context['role'] = role
    if freelancer:
        context['freelancer'] = freelancer
    if tasks:
        context['tasks'] = tasks
    if talent:
        context['talent'] = talent
    if form:
        context['form'] = form
    return context
