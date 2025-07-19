from django.shortcuts import render
from django.http import JsonResponse
from .models import Proveedor
import json
from datetime import datetime

def proveedores(request):
    return render(request, 'Proveedores/proveedores.html')

def listado_proveedores(request):
    proveedores = list(Proveedor.objects.values())
    return JsonResponse({'proveedores': proveedores})

def nuevo_proveedor(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            ruc = request.POST.get('ruc')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('direccion')
            email = request.POST.get('email')
            foto = request.FILES.get('foto')

            # Validar RUC único
            if Proveedor.objects.filter(ruc=ruc).exists():
                return JsonResponse({'error': 'El RUC ya está registrado'}, status=400)

            proveedor = Proveedor.objects.create(
                nombre=nombre,
                ruc=ruc,
                telefono=telefono,
                direccion=direccion,
                email=email,
                foto=foto
            )

            return JsonResponse({
                'mensaje': 'Proveedor creado correctamente',
                'proveedor_id': proveedor.id
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def detalle_proveedor(request, id):
    try:
        proveedor = Proveedor.objects.get(id=id)
        data = {
            'proveedor': {
                'id': proveedor.id,
                'nombre': proveedor.nombre,
                'ruc': proveedor.ruc,
                'telefono': proveedor.telefono,
                'direccion': proveedor.direccion,
                'email': proveedor.email,
                'fecha_creacion': proveedor.fecha_creacion.strftime('%Y-%m-%d'),
                'foto': proveedor.foto.name if proveedor.foto else None
            }
        }
        return JsonResponse(data)
    except Proveedor.DoesNotExist:
        return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)

def editar_proveedor(request, id):
    if request.method == 'POST':
        try:
            proveedor = Proveedor.objects.get(id=id)
            proveedor.nombre = request.POST.get('nombre')
            proveedor.telefono = request.POST.get('telefono')
            proveedor.direccion = request.POST.get('direccion')
            proveedor.email = request.POST.get('email')
            
            # Verificar si se envió una nueva foto
            if 'foto' in request.FILES:
                nueva_foto = request.FILES['foto']
                # Eliminar la foto anterior si existe
                if proveedor.foto:
                    proveedor.foto.delete(save=False)
                proveedor.foto = nueva_foto
            
            proveedor.save()
            
            return JsonResponse({
                'mensaje': 'Proveedor actualizado correctamente',
                'proveedor_id': proveedor.id
            })
            
        except Proveedor.DoesNotExist:
            return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def eliminar_proveedor(request, id):
    if request.method == 'POST':
        try:
            proveedor = Proveedor.objects.get(id=id)
            # Eliminar la foto si existe
            if proveedor.foto:
                proveedor.foto.delete(save=False)
            proveedor.delete()
            return JsonResponse({'mensaje': 'Proveedor eliminado correctamente'})
        except Proveedor.DoesNotExist:
            return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)