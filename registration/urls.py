# registration/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('register/', views.register_view, name='register'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
]