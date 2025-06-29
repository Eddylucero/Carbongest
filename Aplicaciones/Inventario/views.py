from django.shortcuts import render, get_object_or_404
from .models import Inventario


def listarInventario(request):
    inventarios = Inventario.objects.select_related('producto').all()

    datos = []
    productos_bajo_stock = []

    for inv in inventarios:
        producto = inv.producto
        nombre = producto.get_nombre_display()
        cantidad_producto = producto.cantidad
        cantidad_disponible = inv.cantidad_disponible

        # Notificar si el stock actual del producto está bajo (producto.cantidad)
        if cantidad_producto <= 5:
            productos_bajo_stock.append({
                'nombre': nombre,
                'cantidad': cantidad_producto
            })


        datos.append({
            'nombre': nombre,
            'cantidad': cantidad_producto,  # Para mostrar en la tabla
            'cantidad_disponible': cantidad_disponible,  # Para alertas y estilos
            'total_pedidos': inv.total_pedidos,
            'total_ventas': inv.total_ventas,
            'ultima_actualizacion': inv.ultima_actualizacion,
            'producto': producto
        })

    return render(request, 'Inventario/inicioInventario.html', {
        'datos': datos,
        'notificaciones': productos_bajo_stock
    })


def detalleInventario(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    return render(request, 'Inventario/detalleInventario.html', {'inventario': inventario})
