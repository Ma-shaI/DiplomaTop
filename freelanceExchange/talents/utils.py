from .models import Talent, HourlyRate
from django.db.models import Q
from users.models import Freelancer


def search_talent(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    rate = HourlyRate.objects.filter(
        rate__iregex=search_query
    )
    talents = Talent.objects.filter(
        Q(is_published=True) &
        (Q(title__iregex=search_query) |
         Q(descriptions__iregex=search_query) |
         Q(hourlyrate__in=rate) |
         Q(skills__title__iregex=search_query)))
    freelancers = Freelancer.objects.distinct().filter(
        Q(talent__in=talents) |
        Q(bio__iregex=search_query)
    )
    return freelancers, search_query
