from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegisterWizard.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('freelancer_login/', FreelanceLogin.as_view(), name='freelancer_login'),
    path('serves_add/', views.serves_add, name='serves_add'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('login/', views.login_user, name='login_user'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('all_messages/', views.all_messages, name='all_messages'),
    path('chat/<str:pk>/', views.chat, name='chat'),
    path('leave_review/<str:pk>/', views.leave_review, name='leave_review'),
    path('language_add/', views.language_add, name='language_add')
]
