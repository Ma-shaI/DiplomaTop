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
    path('login/', views.login_user, name='login_user')
]
