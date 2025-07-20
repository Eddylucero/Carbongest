from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido, DetallePedido
from collections import defaultdict
from Aplicaciones.Clientes.models import Cliente
from Aplicaciones.Productos.models import Producto
from Aplicaciones.Inventario.models import Inventario
from django.http import JsonResponse
from django.db.models import Sum, Count

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

def graficosPedidos(request):
    return render(request, 'Pedidos/graficos.html')

def datosGraficosPedidos(request):
    # Productos vendidos
    productos_raw = DetallePedido.objects.values('producto__nombre') \
        .annotate(total=Sum('cantidad')) \
        .order_by('-total')
    productos = {
        'labels': [p['producto__nombre'] for p in productos_raw],
        'data': [int(p['total']) for p in productos_raw]
    }

    # Estado de pedidos
    estado = {
        'entregado': Pedido.objects.filter(estado='entregado').count(),
        'cancelado': Pedido.objects.filter(estado='cancelado').count(),
        'pendiente': Pedido.objects.exclude(estado__in=['entregado', 'cancelado']).count()
    }

    # Pedidos por mes
    meses = defaultdict(int)
    pedidos = Pedido.objects.values('fecha_pedido')
    for p in pedidos:
        fecha = p['fecha_pedido']
        if fecha:
            mes = fecha.strftime('%B %Y')  # Ejemplo: "July 2025"
            meses[mes] += 1

    mensual = {
        'labels': list(meses.keys()),
        'data': list(meses.values())
    }

    return JsonResponse({
        'productos': productos,
        'estado': estado,
        'mensual': mensual
    })

def calendarioPedidos(request):
    return render(request, 'Pedidos/calendario.html')

def eventosPedidos(request):
    pedidos = Pedido.objects.select_related('cliente').all()
    eventos = []

    for pedido in pedidos:
        color = '#f1c40f'  # pendiente por defecto
        if pedido.estado == "entregado":
            color = '#2ecc71'
        elif pedido.estado == "cancelado":
            color = '#e74c3c'

        eventos.append({
            'title': f"{pedido.cliente.nombre} ({pedido.estado})",
            'start': pedido.fecha_pedido.strftime('%Y-%m-%d'),
            'color': color
        })


    return JsonResponse(eventos, safe=False)