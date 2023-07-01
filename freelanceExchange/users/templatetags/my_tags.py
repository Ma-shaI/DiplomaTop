from django import template

register = template.Library()


@register.filter
def rating_stars(rating):
    return '★' * rating + '☆' * (5 - rating)


register.filter('rating_stars', rating_stars)