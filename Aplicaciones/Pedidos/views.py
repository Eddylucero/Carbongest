from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido, DetallePedido
from Aplicaciones.Clientes.models import Cliente
from Aplicaciones.Productos.models import Producto
from Aplicaciones.Inventario.models import Inventario

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

            inventario, _ = Inventario.objects.get_or_create(producto=producto)

            if cantidad > producto.cantidad:
                messages.error(request, f"No hay suficiente stock de '{producto.get_nombre_display()}'. Disponible: {producto.cantidad}")
                pedido.delete()
                return redirect('nuevoPedido')

            precio = producto.precio
            subtotal = round(precio * cantidad, 2)

            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio,
                subtotal=subtotal
            )

            producto.cantidad -= cantidad
            producto.save()

            inventario.cantidad_disponible -= cantidad
            inventario.total_pedidos += cantidad
            inventario.save()

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


# Procesar ventas o cancelación
def ventasPedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    detalles = DetallePedido.objects.filter(pedido=pedido)

    if request.method == "POST":
        nuevo_estado = request.POST.get('estado')

        if nuevo_estado == "cancelado":
            for detalle in detalles:
                producto = detalle.producto
                producto.cantidad += detalle.cantidad
                producto.save()

                inventario, _ = Inventario.objects.get_or_create(producto=producto)
                inventario.cantidad_disponible += detalle.cantidad
                inventario.total_pedidos -= detalle.cantidad
                inventario.save()

            pedido.estado = "cancelado"
            pedido.save()
            messages.success(request, "Pedido cancelado y stock restablecido.")
            return redirect('listarPedidos')

        elif nuevo_estado == "entregado":
            for detalle in detalles:
                inventario, _ = Inventario.objects.get_or_create(producto=detalle.producto)
                inventario.total_ventas += detalle.cantidad
                inventario.save()

            pedido.estado = "entregado"
            pedido.save()
            messages.success(request, "Venta confirmada exitosamente.")
            return redirect('listarPedidos')

        else:
            messages.warning(request, "Selecciona un estado válido.")
            return redirect('ventasPedido', id=pedido.id)

    return render(request, 'Pedidos/ventasPedido.html', {
        'pedido': pedido,
        'detalles': detalles
    })
