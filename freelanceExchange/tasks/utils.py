from .models import *
from django.db.models import Q


def search_tasks(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    budget = Budget.objects.filter(
        Q(min_price__iregex=search_query) |
        Q(max_price__iregex=search_query) |
        Q(fix_price__iregex=search_query)
    )
    tasks = Task.objects.distinct().filter(
        Q(is_published=True) &
        (Q(title__iregex=search_query) |
         Q(experiences__iregex=search_query) |
         Q(description__iregex=search_query) |
         Q(budget__in=budget) |
         Q(skills__title__iregex=search_query))

    )
    return tasks, search_query
