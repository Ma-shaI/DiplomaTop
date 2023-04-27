from django import template
from users.models import Services

register = template.Library()


@register.inclusion_tag('base/subnav.html', takes_context=True)
def show_menu_items(context):
    menu_items = Services.objects.all()
    return {
        'service': menu_items
    }
