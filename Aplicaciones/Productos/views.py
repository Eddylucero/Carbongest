from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto

# Listar todos los productos
def listarProductos(request):
    productos = Producto.objects.all()
    return render(request, 'Productos/inicioProductos.html', {'productos': productos})

# Mostrar formulario para nuevo producto
def nuevoProducto(request):
    return render(request, 'Productos/nuevoProducto.html')

# Guardar o actualizar cantidad de un producto existente
def guardarProducto(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        peso = request.POST.get('peso')
        presentacion = request.POST.get('presentacion')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')

        if not nombre or not precio:
            messages.warning(request, "El nombre y el precio son obligatorios.")
            return redirect('nuevoProducto')

        try:
            cantidad = int(cantidad)
            peso = float(peso)
            precio = float(precio)
        except ValueError:
            messages.warning(request, "Verifica que los campos numéricos sean válidos.")
            return redirect('nuevoProducto')

        producto_existente = Producto.objects.filter(
            nombre=nombre,
            presentacion=presentacion
        ).first()

        if producto_existente:
            producto_existente.cantidad += cantidad
            producto_existente.precio = precio  # opcional: actualiza precio
            producto_existente.tipo = tipo
            producto_existente.peso = peso
            producto_existente.save()
            messages.success(request, "Cantidad agregada al producto existente.")
        else:
            Producto.objects.create(
                nombre=nombre,
                tipo=tipo,
                peso=peso,
                presentacion=presentacion,
                precio=precio,
                cantidad=cantidad
            )
            messages.success(request, "Producto registrado correctamente.")

        return redirect('listarProductos')

    return redirect('listarProductos')

# Eliminar producto
def eliminarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Producto eliminado.")
    return redirect('listarProductos')

# Mostrar producto para editar
def editarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    print(">>> peso:", producto.peso)
    print(">>> precio:", producto.precio)
    return render(request, 'Productos/editarProducto.html', {'producto': producto})

# Actualizar producto editado
def actualizarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        try:
            producto.nombre = request.POST.get('nombre')
            producto.tipo = request.POST.get('tipo')

            # Reemplaza la coma por punto antes de convertir
            peso_str = request.POST.get('peso').replace(',', '.')
            precio_str = request.POST.get('precio').replace(',', '.')

            producto.peso = float(peso_str)
            producto.precio = float(precio_str)

            producto.presentacion = request.POST.get('presentacion')
            producto.cantidad = int(request.POST.get('cantidad'))

            producto.save()
            messages.success(request, "Producto actualizado correctamente.")
        except Exception as e:
            messages.warning(request, f"Error al actualizar: {e}")

        return redirect('listarProductos')

    return redirect('listarProductos')
