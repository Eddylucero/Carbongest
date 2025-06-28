from django.urls import path
from . import views

urlpatterns = [
    path('', views.listarPedidos, name='listarPedidos'),
    path('nuevoPedido/', views.nuevoPedido, name='nuevoPedido'),
    path('guardarPedido/', views.guardarPedido, name='guardarPedido'),
    path('detallePedido/<int:id>/', views.detallePedido, name='detallePedido'),
    path('eliminarPedido/<int:id>/', views.eliminarPedido, name='eliminarPedido'),
    path('ventasPedido/<int:id>/', views.ventasPedido, name='ventasPedido'),  # 🔥 nueva ruta
]
