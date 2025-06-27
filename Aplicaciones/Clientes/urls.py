from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicioClientes, name='inicioClientes'),
]