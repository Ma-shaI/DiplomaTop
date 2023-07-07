from django.shortcuts import render
from .utils import get_messages


def index(request):
    context = get_messages(request.user.profile)
    return render(request, 'base/index.html', context)
