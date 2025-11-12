from django.urls import path
from .views import register, login

urlpatterns = [
    path('register', register),  # Cambiado: /register → register
    path('login', login),        # Cambiado: /login → login
]