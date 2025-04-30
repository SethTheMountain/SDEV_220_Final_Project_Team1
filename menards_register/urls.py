<<<<<<< HEAD
=======
# menards_register/urls.py
>>>>>>> 5bac7396538c333b6b061a6a48f0cb071cbf1da0
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registration.urls')),
]