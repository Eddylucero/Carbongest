from django.urls import path
from . import views

urlpatterns = [
    path('', views.listarClientes, name='listarClientes'),
    path('nuevoCliente/', views.nuevoCliente, name='nuevoCliente'),
    path('guardarCliente/', views.guardarCliente, name='guardarCliente'),
    path('eliminarCliente/<int:id>/', views.eliminarCliente, name='eliminarCliente'),
    path('editarCliente/<int:id>/', views.editarCliente, name='editarCliente'),
    path('actualizarCliente/<int:id>/', views.actualizarCliente, name='actualizarCliente'),
]
