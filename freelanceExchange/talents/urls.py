from django.urls import path
from . import views

urlpatterns = [
    path('talent_add/', views.talent_add, name='talent_add'),
    path('talent_update/<str:pk>/', views.talent_update, name='talent_update'),
    path('talent_delete/<str:pk>/', views.talent_delete, name='talent_delete'),
    path('find_talent/', views.find_talent, name='find_talent'),
    path('liked_talent/<str:pk>/', views.liked_talent, name='liked_talent'),
    path('saved_talents/', views.saved_talents, name='saved_talents')
]
