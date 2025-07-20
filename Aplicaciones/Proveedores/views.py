import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings # Para acceder a TELEGRAM_BOT_TOKEN

from .models import Proveedor

# Vistas existentes (mantener igual)
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
            return JsonResponse({'mensaje': 'Proveedor creado correctamente', 'proveedor_id': proveedor.id})
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
            
            if 'foto' in request.FILES:
                nueva_foto = request.FILES['foto']
                if proveedor.foto:
                    proveedor.foto.delete(save=False)
                proveedor.foto = nueva_foto
            
            proveedor.save()
            return JsonResponse({'mensaje': 'Proveedor actualizado correctamente', 'proveedor_id': proveedor.id})
            
        except Proveedor.DoesNotExist:
            return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def eliminar_proveedor(request, id):
    if request.method == 'POST':
        try:
            proveedor = Proveedor.objects.get(id=id)
            if proveedor.foto:
                proveedor.foto.delete(save=False)
            proveedor.delete()
            return JsonResponse({'mensaje': 'Proveedor eliminado correctamente'})
        except Proveedor.DoesNotExist:
            return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


# Nueva vista para mostrar el formulario de envío de Telegram
def envio_telegram(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)

    
    return render(request, 'Proveedores/envioProveedor.html', {
        'proveedor': proveedor,
        'productos': ['Pino', 'Eucalipto', 'Otro']
    })

# Vista para procesar el envío del pedido por Telegram
def procesar_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            proveedor = get_object_or_404(Proveedor, pk=data.get('proveedor_id'))
            
            chat_id = proveedor.telegram_chat_id # Usamos el chat_id almacenado en el modelo
            
            if not chat_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El proveedor no tiene un chat de Telegram vinculado. Pídale que inicie chat con el bot y se registre.'
                }, status=400)
            
            # Construir mensaje
            producto1 = data.get('producto1')
            metros1 = data.get('metros1')
            mensaje_adicional = data.get('mensaje_adicional', '')

            mensaje = (
                f"📦 *NUEVO PEDIDO PARA {proveedor.nombre.upper()}*\n\n"
                f"🔹 *Producto solicitado:* {producto1}\n"
                f"🔹 *Cantidad:* {metros1} m³\n"
            )

            if mensaje_adicional:
                mensaje += f"\n📝 *Observaciones adicionales:*\n{mensaje_adicional}\n"

            mensaje += "\nPor favor, confirme este pedido a la brevedad. ✅"
            
            # Enviar mensaje vía Telegram API
            bot_token = settings.TELEGRAM_BOT_TOKEN
            send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            response = requests.post(send_url, json={
                'chat_id': chat_id,
                'text': mensaje,
                'parse_mode': 'Markdown' # Para negritas, cursivas, etc.
            })
            
            if response.status_code != 200:
                error_data = response.json()
                error_msg = error_data.get('description', 'Error desconocido de Telegram')
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error al enviar a Telegram: {error_msg}. Posiblemente el chat_id es incorrecto o el bot no tiene permiso.'
                }, status=400)
                
            return JsonResponse({
                'status': 'success',
                'message': 'Pedido enviado correctamente a Telegram.'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Solicitud JSON inválida.'}, status=400)
        except Proveedor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Proveedor no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error interno del servidor: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)