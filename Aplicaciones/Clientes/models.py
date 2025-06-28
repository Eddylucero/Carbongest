from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula_o_ruc = models.CharField(max_length=13, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    referencia = models.TextField(blank=True, null=True)

    tipo_cliente = models.CharField(
        max_length=20,
        choices=[
            ('frecuente', 'Frecuente'),
            ('ocasional', 'Ocasional'),
            ('mayorista', 'Mayorista'),
            ('minorista', 'Minorista'),
        ],
        default='ocasional'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.cedula_o_ruc})"