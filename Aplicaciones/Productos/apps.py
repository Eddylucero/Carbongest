from django.apps import AppConfig

class ProductosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Aplicaciones.Productos'

    def ready(self):
        import Aplicaciones.Productos.signals
