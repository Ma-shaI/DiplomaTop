from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('task_add/', TaskWizard.as_view(), name='task_add'),
    path('task_budget/<str:pk>/', views.task_budget, name='task_budget'),
    path('find_work/', views.find_work, name='find_work'),
    path('like_task/', views.like_task, name='like_task'),
    path('task/<str:pk>/', views.task, name='task'),
    path('saved_tasks/', views.saved_tasks, name='saved_tasks'),
    path('offers/', views.my_offers, name='offers'),
    path('my_tasks/', views.my_tasks, name='my_tasks'),
    path('delete_task/<str:pk>/', views.delete_task, name='delete_task'),
    path('update_task/<str:pk>/', views.update_task, name='update_task'),
    path('send_offer/', views.send_offer, name='send_offer'),
    path('accept_offer/<str:pk>/', views.accept_offer, name='accept_offer'),
    path('my_staff/', views.my_staff, name='my_staff'),
    path('work/<str:pk>/', views.work, name='work'),
    path('add_stage/', views.add_stage, name='add_stage')
]
