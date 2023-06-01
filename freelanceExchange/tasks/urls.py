from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('task_add/', TaskWizard.as_view(), name='task_add'),
    path('task_budget/<str:pk>/', views.task_budget, name='task_budget')
]
