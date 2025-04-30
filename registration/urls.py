# registration/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),  # Root URL for the main page
    path('main/', views.main, name='main'),
    path('set_timezone/', views.set_timezone, name='set_timezone'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('custom_admin/', views.custom_admin, name='custom_admin'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
]