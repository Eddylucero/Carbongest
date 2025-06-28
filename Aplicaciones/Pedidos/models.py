from django.db import models
from Aplicaciones.Clientes.models import Cliente
from Aplicaciones.Productos.models import Producto

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('entregado', 'Entregado'),
            ('cancelado', 'Cancelado'),
        ],
        default='pendiente'
    )
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.get_nombre_display()} ({self.producto.presentacion}) x {self.cantidad}"
