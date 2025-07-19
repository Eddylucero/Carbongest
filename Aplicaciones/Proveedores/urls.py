from django.urls import path
from . import views

urlpatterns = [
    path('', views.proveedores, name='proveedores'),
    path('listado/', views.listado_proveedores, name='listado_proveedores'),
    path('nuevo/', views.nuevo_proveedor, name='nuevo_proveedor'),
    path('detalle/<int:id>/', views.detalle_proveedor, name='detalle_proveedor'),
    path('editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
]