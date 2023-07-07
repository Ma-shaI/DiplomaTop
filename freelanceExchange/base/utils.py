from tasks.models import Offers
from users.models import Message


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
