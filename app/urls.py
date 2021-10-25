from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('agregar_paquetes/<int:id>/', views.agregar_paquetes, name='agregar_paquetes'),
]