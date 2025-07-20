from django.test import TestCase, Client
from django.urls import reverse
from Aplicaciones.Pedidos.models import Pedido, DetallePedido
from Aplicaciones.Clientes.models import Cliente
from Aplicaciones.Productos.models import Producto
from Aplicaciones.Inventario.models import Inventario
from datetime import datetime

class PedidoViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.cliente = Cliente.objects.create(
            nombre="Luis T",
            cedula_o_ruc="1234567890",
            direccion="Av. Principal",
            ciudad="Pujilí",
            provincia="Cotopaxi",
            tipo_cliente="frecuente"
        )
        self.producto = Producto.objects.create(
            nombre="Chocolate",
            tipo="procesado",
            peso=10,
            precio=2.50,
            cantidad=20
        )
        self.inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad_disponible=20,
            total_pedidos=0,
            total_ventas=0,
            ultima_actualizacion=datetime.now()
        )

    def test_listarPedidos(self):
        Pedido.objects.create(cliente=self.cliente, observacion="Prueba de pedido")
        response = self.client.get(reverse('listarPedidos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Pedidos/inicioPedidos.html')
        self.assertContains(response, self.cliente.nombre)
        print("✅ test_listarPedidos pasó correctamente.")

    def test_nuevoPedido(self):
        response = self.client.get(reverse('nuevoPedido'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Pedidos/nuevoPedido.html')
        self.assertContains(response, self.producto.get_nombre_display())
        print("✅ test_nuevoPedido pasó correctamente.")

    def test_guardarPedido(self):
        data = {
            'cliente': self.cliente.id,
            'observacion': 'Pedido de prueba',
            'producto[]': [str(self.producto.id)],
            'cantidad[]': ['5']
        }
        response = self.client.post(reverse('guardarPedido'), data)
        self.assertEqual(response.status_code, 302)
        pedido_creado = Pedido.objects.last()
        self.assertEqual(pedido_creado.cliente.id, self.cliente.id)
        self.assertEqual(DetallePedido.objects.filter(pedido=pedido_creado).count(), 1)
        print("✅ test_guardarPedido pasó correctamente.")

    def test_detallePedido(self):
        pedido = Pedido.objects.create(cliente=self.cliente)
        DetallePedido.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=2,
            precio_unitario=2.50,
            subtotal=5.00
        )
        response = self.client.get(reverse('detallePedido', args=[pedido.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Pedidos/detallePedido.html')
        self.assertContains(response, self.producto.get_nombre_display())
        print("✅ test_detallePedido pasó correctamente.")

    def test_eliminarPedido(self):
        pedido = Pedido.objects.create(cliente=self.cliente)
        response = self.client.get(reverse('eliminarPedido', args=[pedido.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pedido.objects.filter(id=pedido.id).exists())
        print("✅ test_eliminarPedido pasó correctamente.")

    def test_ventasPedido_cancelado(self):
        pedido = Pedido.objects.create(cliente=self.cliente)
        DetallePedido.objects.create(pedido=pedido, producto=self.producto, cantidad=3, precio_unitario=2.50, subtotal=7.50)
        pedido.estado = "pendiente"
        pedido.save()
        data = {'estado': 'cancelado'}
        response = self.client.post(reverse('ventasPedido', args=[pedido.id]), data)
        self.assertRedirects(response, reverse('listarPedidos'))
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, 'cancelado')
        print("✅ test_ventasPedido_cancelado pasó correctamente.")

    def test_ventasPedido_entregado(self):
        pedido = Pedido.objects.create(cliente=self.cliente)
        DetallePedido.objects.create(pedido=pedido, producto=self.producto, cantidad=4, precio_unitario=2.50, subtotal=10.00)
        data = {'estado': 'entregado'}
        response = self.client.post(reverse('ventasPedido', args=[pedido.id]), data)
        self.assertRedirects(response, reverse('listarPedidos'))
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, 'entregado')
        print("✅ test_ventasPedido_entregado pasó correctamente.")
