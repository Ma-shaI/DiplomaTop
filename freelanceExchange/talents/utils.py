from .models import Talent
from django.db.models import Q
from users.models import Freelancer


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
