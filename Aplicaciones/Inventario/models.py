from django.db import models
from Aplicaciones.Productos.models import Producto

class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0, help_text="Cantidad mínima antes de alertar")
    stock_maximo = models.IntegerField(blank=True, null=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_disponible}"
