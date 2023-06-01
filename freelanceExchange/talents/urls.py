from django.urls import path
from . import views



urlpatterns = [
    path('talent_add', views.talent_add, name='talent_add'),
]