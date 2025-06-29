from Aplicaciones.Inventario.models import Inventario

def notificaciones_inventario(request):
    productos_bajo_stock = []

    inventarios = Inventario.objects.select_related('producto').all()
    for inv in inventarios:
        producto = inv.producto
        if producto.cantidad <= 5:  # o inv.cantidad_disponible si prefieres eso
            productos_bajo_stock.append({
                'nombre': producto.get_nombre_display(),
                'cantidad': producto.cantidad
            })

    return {
        'notificaciones': productos_bajo_stock
    }
