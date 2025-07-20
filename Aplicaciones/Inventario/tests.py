from django.test import TestCase, Client
from django.urls import reverse
from Aplicaciones.Inventario.models import Inventario
from Aplicaciones.Productos.models import Producto
from datetime import datetime

class InventarioViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Crear producto simulado
        self.producto = Producto.objects.create(
            nombre='Cacao Premium',
            tipo='Materia Prima',
            peso=25,
            precio=42.50,
            cantidad=3  # Bajo stock para alerta
        )
        # Crear inventario asociado al producto
        self.inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad_disponible=2,
            total_pedidos=10,
            total_ventas=7,
            ultima_actualizacion=datetime.now()
        )

    def test_listarInventario(self):
        response = self.client.get(reverse('listarInventario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Inventario/inicioInventario.html')
        self.assertContains(response, 'Cacao Premium')
        self.assertIn('notificaciones', response.context)
        self.assertGreaterEqual(len(response.context['notificaciones']), 1)
        print("✅ test_listarInventario pasó correctamente.")

    def test_detalleInventario(self):
        response = self.client.get(reverse('detalleInventario', args=[self.inventario.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Inventario/detalleInventario.html')
        self.assertEqual(response.context['inventario'].producto.nombre, 'Cacao Premium')
        print("✅ test_detalleInventario pasó correctamente.")
