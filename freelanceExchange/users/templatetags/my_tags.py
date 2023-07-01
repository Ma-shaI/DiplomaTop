from django import template
from django.db.models import Avg
register = template.Library()

@register.filter
def rating_stars(rating):
    return '★' * rating + '☆' * (5 - rating)


@register.filter(name='average_rating')
def average_rating(qs):
    return round((qs.aggregate(Avg('rating'))['rating__avg']), 2)
