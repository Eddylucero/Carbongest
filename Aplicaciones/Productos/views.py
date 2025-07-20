from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
import os
from django.conf import settings
from django.contrib.auth.decorators import permission_required

def listarProductos(request):
    productos = Producto.objects.all()
    return render(request, 'Productos/inicioProductos.html', {'productos': productos})


def nuevoProducto(request):
    return render(request, 'Productos/nuevoProducto.html')


def guardarProducto(request):
    if request.method == "POST":
        try:
            nombre = request.POST.get('nombre')
            tipo = request.POST.get('tipo')
            presentacion = request.POST.get('presentacion')
            peso = request.POST.get('peso', '0')
            precio = request.POST.get('precio', '0')
            cantidad = request.POST.get('cantidad', '0')
            foto = request.FILES.get('foto')  # Obtenemos la imagen

            if not all([nombre, tipo, presentacion, peso, precio, cantidad]):
                return redirect('nuevoProducto')

            peso_limpio = ''.join(filter(lambda x: x.isdigit() or x == '.', peso))
            
            try:
                peso = float(peso_limpio) if peso_limpio else 0.0
                precio = float(precio) if precio else 0.0
                cantidad = int(cantidad) if cantidad else 0
            except (ValueError, TypeError):
                return redirect('nuevoProducto')

            producto_existente = Producto.objects.filter(
                nombre=nombre,
                tipo=tipo,
                presentacion=presentacion
            ).first()

            if producto_existente:
                producto_existente.cantidad += cantidad
                producto_existente.precio = precio
                if foto:  # Si se sube nueva foto, actualizarla
                    if producto_existente.foto:
                        # Eliminar la foto anterior
                        if os.path.isfile(producto_existente.foto.path):
                            os.remove(producto_existente.foto.path)
                    producto_existente.foto = foto
                producto_existente.save()
                messages.success(request, f"Se agregaron {cantidad} unidades al producto existente")
            else:
                Producto.objects.create(
                    nombre=nombre,
                    tipo=tipo,
                    presentacion=presentacion,
                    peso=peso,
                    precio=precio,
                    cantidad=cantidad,
                    foto=foto  # Guardar la imagen
                )
                messages.success(request, "Producto creado exitosamente")

            return redirect('listarProductos')

        except Exception as e:
            messages.error(request, f"Error al guardar: {str(e)}")
            return redirect('nuevoProducto')

    return redirect('listarProductos')

@permission_required('productos.delete_producto', raise_exception=True)
def eliminarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    # La eliminación de la imagen se maneja en el método delete() del modelo
    producto.delete()
    messages.success(request, "Producto eliminado correctamente")
    return redirect('listarProductos')


def editarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)

    return render(request, 'Productos/editarProducto.html', {'producto': producto})


def actualizarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        try:
            #producto.nombre = request.POST.get('nombre')

            producto.tipo = request.POST.get('tipo')

            producto.presentacion = request.POST.get('presentacion')

            peso_str = request.POST.get('peso', '0').replace(',', '.')
            producto.peso = float(''.join(filter(lambda x: x.isdigit() or x == '.', peso_str))) if peso_str else 0.0
            
            precio_str = request.POST.get('precio', '0').replace(',', '.')
            producto.precio = float(precio_str) if precio_str else 0.0
            
            cantidad_str = request.POST.get('cantidad', '0')
            producto.cantidad = int(cantidad_str) if cantidad_str else 0

            # Manejo de la nueva imagen
            if 'foto' in request.FILES:
                nueva_foto = request.FILES['foto']
                # Eliminar la foto anterior si existe
                if producto.foto:
                    if os.path.isfile(producto.foto.path):
                        os.remove(producto.foto.path)
                producto.foto = nueva_foto

            producto.save()
            messages.success(request, "Producto actualizado correctamente")
        except Exception as e:
            messages.error(request, f"Error al actualizar: {str(e)}")

        return redirect('listarProductos')

    return redirect('listarProductos')
