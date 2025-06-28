from django.db import models

class Producto(models.Model):
    OPCIONES_NOMBRE = [
        ('carbon_vegetal', 'Carbón Vegetal'),
        ('carbon_mineral', 'Carbón Mineral'),
        ('leña_dura', 'Leña Dura'),
        ('leña_suave', 'Leña Suave'),
    ]

    nombre = models.CharField(max_length=50, choices=OPCIONES_NOMBRE)
    tipo = models.CharField(max_length=50)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    presentacion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    cantidad = models.IntegerField(default=0)  # <- Aquí controlas el stock acumulado

    def __str__(self):
        return f"{self.get_nombre_display()} ({self.presentacion})"
