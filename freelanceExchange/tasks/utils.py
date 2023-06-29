from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_tasks(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tasks = Task.objects.distinct().filter(
        Q(is_published=True) &
        (Q(title__icontains=search_query) |
         Q(experiences__icontains=search_query) |
         Q(description__icontains=search_query) |
         Q(skills__title__icontains=search_query))
    )
    return tasks, search_query
