from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido, DetallePedido
from Aplicaciones.Clientes.models import Cliente
from Aplicaciones.Productos.models import Producto

# Listar pedidos
def listarPedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'Pedidos/inicioPedidos.html', {'pedidos': pedidos})

# Crear nuevo pedido
def nuevoPedido(request):
    clientes = Cliente.objects.all()
    productos = Producto.objects.all()
    return render(request, 'Pedidos/nuevoPedido.html', {
        'clientes': clientes,
        'productos': productos
    })

# Guardar pedido
def guardarPedido(request):
    if request.method == "POST":
        cliente_id = request.POST.get('cliente')
        observacion = request.POST.get('observacion')

        cliente = get_object_or_404(Cliente, id=cliente_id)
        pedido = Pedido.objects.create(cliente=cliente, observacion=observacion)

        productos = request.POST.getlist('producto[]')
        cantidades = request.POST.getlist('cantidad[]')

        for i in range(len(productos)):
            producto = Producto.objects.get(id=productos[i])
            cantidad = int(cantidades[i])

            # Validar stock
            if cantidad > producto.cantidad:
                messages.error(request, f"No hay suficiente stock de '{producto.get_nombre_display()}'. Disponible: {producto.cantidad}")
                pedido.delete()
                return redirect('nuevoPedido')

            precio = producto.precio
            subtotal = round(precio * cantidad, 2)

            # Crear detalle y descontar stock
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio,
                subtotal=subtotal
            )

            producto.cantidad -= cantidad
            producto.save()

        messages.success(request, "Pedido registrado y stock actualizado correctamente.")
        return redirect('listarPedidos')

    return redirect('listarPedidos')

# Ver detalle del pedido
def detallePedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'Pedidos/detallePedido.html', {
        'pedido': pedido,
        'detalles': detalles
    })

# Eliminar pedido
def eliminarPedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.delete()
    messages.success(request, "Pedido eliminado.")
    return redirect('listarPedidos')
