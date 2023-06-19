from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('task_add/', TaskWizard.as_view(), name='task_add'),
    path('task_budget/<str:pk>/', views.task_budget, name='task_budget'),
    path('find_work/', views.find_work, name='find_work'),
    path('liked_task/', views.liked_tasks, name='liked_task'),
    path('task/<str:pk>/', views.task, name='task'),
    path('saved_tasks/', views.saved_tasks, name='saved_tasks'),
    path('offers/', views.offers, name='offers')
]
