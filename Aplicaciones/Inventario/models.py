from django.db import models
from Aplicaciones.Productos.models import Producto

class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField(default=0)
    total_pedidos = models.IntegerField(default=0, help_text="Acumulado de unidades pedidas")
    total_ventas = models.IntegerField(default=0, help_text="Acumulado de unidades vendidas")
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto.get_nombre_display()} - {self.cantidad_disponible} ud"
