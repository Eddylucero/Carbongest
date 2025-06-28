from django.shortcuts import render, get_object_or_404
from .models import Inventario
from django.contrib import messages
from .models import Producto


# Ver listado de inventario
def listarInventario(request):
    inventarios = Inventario.objects.select_related('producto').all()
    return render(request, 'Inventario/inicioInventario.html', {'inventarios': inventarios})

# Vista detallada de un producto en inventario (opcional)
def detalleInventario(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    return render(request, 'Inventario/detalleInventario.html', {'inventario': inventario})
