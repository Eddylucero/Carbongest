from django.db import models

# Create your models here.
class Registro(models.Model):
    nombre_usuario = models.CharField(max_length=150, unique=True)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_usuario
