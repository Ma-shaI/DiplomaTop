from tasks.models import Offers
from users.models import Message
from django.core.paginator import Paginator


def get_messages(user):
    received_messages = Message.objects.filter(recipient=user)
    unread_count = received_messages.filter(is_read=False).count()
    try:
        offers = Offers.objects.filter(prospective_employee=user.freelancer).filter(at_work=False).count()
    except:
        offers = ''
    return {
        'unread_count': unread_count,
        'offers_count': offers
    }


def paginate_data(request, model, results):
    page = request.GET.get('page', 1)
    paginator = Paginator(model, results)

    model = paginator.get_page(page)
    left_index = int(page) - 4

    if left_index < 1:
        left_index = 1
    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    return model, custom_range
