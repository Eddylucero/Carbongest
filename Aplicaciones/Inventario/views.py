from django.shortcuts import render, get_object_or_404
from .models import Inventario
from django.contrib import messages
from .models import Producto


def listarInventario(request):
    inventarios = Inventario.objects.select_related('producto').all()

    datos = []
    for inv in inventarios:
        datos.append({
            'nombre': inv.producto.get_nombre_display(),
            'cantidad': inv.producto.cantidad,
            'total_pedidos': inv.total_pedidos,
            'total_ventas': inv.total_ventas,
            'ultima_actualizacion': inv.ultima_actualizacion,
        })

    return render(request, 'Inventario/inicioInventario.html', {'datos': datos})

# Vista detallada de un producto en inventario (opcional)
def detalleInventario(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    return render(request, 'Inventario/detalleInventario.html', {'inventario': inventario})
