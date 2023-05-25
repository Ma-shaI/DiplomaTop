from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegisterWizard.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
]
