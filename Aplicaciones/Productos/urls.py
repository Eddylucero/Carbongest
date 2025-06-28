from django.urls import path
from . import views

urlpatterns = [
    path('', views.listarProductos, name='listarProductos'),
    path('nuevoProducto/', views.nuevoProducto, name='nuevoProducto'),
    path('guardarProducto/', views.guardarProducto, name='guardarProducto'),
    path('editarProducto/<int:id>/', views.editarProducto, name='editarProducto'),
    path('actualizarProducto/<int:id>/', views.actualizarProducto, name='actualizarProducto'),
    path('eliminarProducto/<int:id>/', views.eliminarProducto, name='eliminarProducto'),
]