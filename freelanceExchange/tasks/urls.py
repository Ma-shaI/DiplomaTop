from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('task_add/', TaskWizard.as_view(), name='task_add'),
    path('task_budget/<str:pk>/', views.task_budget, name='task_budget'),
    path('find_work/', views.find_work, name='find_work'),
    path('saved_tasks/', views.saved_tasks, name='saved_tasks'),
    path('task/<str:pk>/', views.task, name='task'),
]
