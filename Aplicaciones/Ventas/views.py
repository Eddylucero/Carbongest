from django.shortcuts import render
from django.http import JsonResponse
from .models import DetalleVenta
from django.db.models import Sum

# Vista que devuelve datos JSON para Chart.js
def ingresoProductos(request):
    datos = DetalleVenta.objects.values('producto__nombre') \
        .annotate(total=Sum('subtotal')) \
        .order_by('-total')

    labels = [item['producto__nombre'] for item in datos]
    data = [float(item['total']) for item in datos]

    return JsonResponse({'labels': labels, 'data': data})

# Vista para renderizar la plantilla de gráficos
def graficos(request):
    return render(request, 'Ventas/graficos.html')
