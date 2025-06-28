from django.urls import path
from . import views

urlpatterns = [
    path('', views.listarInventario, name='listarInventario'),
    path('detalle/<int:id>/', views.detalleInventario, name='detalleInventario'),
]
