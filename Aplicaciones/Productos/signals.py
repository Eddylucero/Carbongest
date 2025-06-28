from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Producto
from Aplicaciones.Inventario.models import Inventario

@receiver(post_save, sender=Producto)
def crear_inventario(sender, instance, created, **kwargs):
    if created:
        Inventario.objects.get_or_create(producto=instance)
