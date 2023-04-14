from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_user, name='register_user'),
    path('reg_start_client', views.reg_start_client, name='reg_start_client'),
    path('reg_client', views.reg_client, name='reg_client'),
    path('reg_start_frlnc', views.reg_start_frlnc, name='reg_start_frlnc'),
    path('reg_freelancer', views.reg_freelancer, name='reg_freelancer'),
]
