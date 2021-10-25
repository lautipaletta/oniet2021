from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('localidades/', views.localidades, name='localidades'),
    path('barrios_graves/', views.barrios_graves, name='barrios_graves'),
    path('barrio/<int:id>', views.barrio, name='barrio'),
    path('agregar_paquetes/<int:id>/', views.agregar_paquetes, name='agregar_paquetes'),
]