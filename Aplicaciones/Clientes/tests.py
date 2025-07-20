from django.test import TestCase, Client
from django.urls import reverse
from Aplicaciones.Clientes.models import Cliente

class ClienteViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Crear cliente base para pruebas
        self.cliente = Cliente.objects.create(
            nombre="Juan Pérez",
            cedula_o_ruc="0102030405",
            telefono="0991234567",
            email="juan@example.com",
            direccion="Calle Falsa 123",
            ciudad="Pujilí",
            provincia="Cotopaxi",
            referencia="Frente al mercado",
            tipo_cliente="frecuente"
        )

    def test_listarClientes(self):
        response = self.client.get(reverse('listarClientes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Clientes/inicioClientes.html')
        self.assertContains(response, 'Juan Pérez')
        print("✅ test_listarClientes pasó correctamente.")

    def test_nuevoCliente(self):
        response = self.client.get(reverse('nuevoCliente'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Clientes/nuevoCliente.html')
        self.assertContains(response, 'Agregar Nuevo Cliente')
        print("✅ test_nuevoCliente pasó correctamente.")

    def test_guardarCliente_post(self):
        data = {
            'nombre': 'Ana Cedeño',
            'cedula_o_ruc': '0987654321',
            'telefono': '0981122334',
            'email': 'ana@example.com',
            'direccion': 'Av. Libertad 456',
            'ciudad': 'Latacunga',
            'provincia': 'Cotopaxi',
            'referencia': 'Cerca del parque',
            'tipo_cliente': 'mayorista'
        }
        response = self.client.post(reverse('guardarCliente'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Cliente.objects.filter(nombre='Ana Cedeño').exists())
        print("✅ test_guardarCliente_post pasó correctamente.")

    def test_guardarCliente_get_redirige(self):
        response = self.client.get(reverse('guardarCliente'))
        self.assertEqual(response.status_code, 302)
        print("✅ test_guardarCliente_get_redirige pasó correctamente.")

    def test_editarCliente(self):
        response = self.client.get(reverse('editarCliente', args=[self.cliente.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Clientes/editarCliente.html')
        self.assertContains(response, 'Juan Pérez')
        print("✅ test_editarCliente pasó correctamente.")

    def test_actualizarCliente_post(self):
        data = {
            'nombre': 'Juan Editado',
            'cedula_o_ruc': self.cliente.cedula_o_ruc,
            'telefono': '0998889999',
            'email': 'juan.editado@example.com',
            'direccion': self.cliente.direccion,
            'ciudad': self.cliente.ciudad,
            'provincia': self.cliente.provincia,
            'referencia': self.cliente.referencia,
            'tipo_cliente': self.cliente.tipo_cliente
        }
        response = self.client.post(reverse('actualizarCliente', args=[self.cliente.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Cliente.objects.filter(nombre='Juan Editado').exists())
        print("✅ test_actualizarCliente_post pasó correctamente.")

    def test_eliminarCliente(self):
        response = self.client.get(reverse('eliminarCliente', args=[self.cliente.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Cliente.objects.filter(id=self.cliente.id).exists())
        print("✅ test_eliminarCliente pasó correctamente.")
