from .models import *
from django.db.models import Q
from django.core.paginator import Paginator


def search_tasks(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tasks = Task.objects.distinct().filter(
        Q(is_published=True) &
        (Q(title__iregex=search_query) |
         Q(experiences__iregex=search_query) |
         Q(description__iregex=search_query) |
         Q(skills__title__iregex=search_query))
    )
    return tasks, search_query


def paginate_tasks(request, tasks, results):
    page = request.GET.get('page', 1)
    paginator = Paginator(tasks, results)

    tasks = paginator.get_page(page)
    left_index = int(page) - 4

    if left_index < 1:
        left_index = 1
    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    return tasks, custom_range
