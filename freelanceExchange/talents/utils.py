from .models import Talent
from django.db.models import Q
from users.models import Freelancer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_talent(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    talents = Talent.objects.filter(
        Q(is_published=True) &
        (Q(title__icontains=search_query) |
         Q(descriptions__icontains=search_query) |
         Q(skills__title__icontains=search_query)))
    freelancers = Freelancer.objects.distinct().filter(
        Q(talent__in=talents)
    )
    return freelancers, search_query


def paginate_talent(request, talents, results):
    page = request.GET.get('page', 1)
    paginator = Paginator(talents, results)

    talents = paginator.get_page(page)
    left_index = int(page) - 4

    if left_index < 1:
        left_index = 1
    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    return talents, custom_range
