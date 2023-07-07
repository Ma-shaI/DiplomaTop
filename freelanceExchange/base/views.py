from django.shortcuts import render
from .utils import get_messages


def index(request):
    try:
        contex = get_messages(request.user.profile)
    except:
        contex={}
    return render(request, 'base/index.html', contex)
