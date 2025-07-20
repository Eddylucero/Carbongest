from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente
from django.contrib.auth.decorators import permission_required

# Listar clientes
def listarClientes(request):
    clientes = Cliente.objects.all()
    for cliente in clientes:
        print(f"Cliente: {cliente.nombre}, Tipo: {cliente.tipo_cliente}")
    return render(request, "Clientes/inicioClientes.html", {'clientes': clientes})


# Mostrar formulario para nuevo cliente
def nuevoCliente(request):
    return render(request, "Clientes/nuevoCliente.html")

# Guardar cliente
def guardarCliente(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        cedula = request.POST.get('cedula_o_ruc', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()
        provincia = request.POST.get('provincia', '').strip()
        referencia = request.POST.get('referencia', '').strip()
        tipo = request.POST.get('tipo_cliente', '').strip()

        if not nombre or not cedula or not direccion:
            messages.warning(request, "Los campos nombre, cédula/RUC y dirección son obligatorios.")
            return redirect('nuevoCliente')

        if Cliente.objects.filter(cedula_o_ruc=cedula).exists():
            messages.error(request, "Ya existe un cliente con esa cédula o RUC.")
            return redirect('nuevoCliente')

        Cliente.objects.create(
            nombre=nombre,
            cedula_o_ruc=cedula,
            telefono=telefono,
            email=email,
            direccion=direccion,
            ciudad=ciudad,
            provincia=provincia,
            referencia=referencia,
            tipo_cliente=tipo
        )
        messages.success(request, "Cliente registrado exitosamente.")
        return redirect('listarClientes')

    return redirect('listarClientes')

@permission_required('clientes.delete_cliente', raise_exception=True)
def eliminarCliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect('listarClientes')

# Editar cliente
def editarCliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return render(request, "Clientes/editarCliente.html", {'cliente': cliente})

# Procesar edición
def actualizarCliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        cliente.nombre = request.POST.get('nombre', '').strip()
        cliente.cedula_o_ruc = request.POST.get('cedula_o_ruc', '').strip()
        cliente.telefono = request.POST.get('telefono', '').strip()
        cliente.email = request.POST.get('email', '').strip()
        cliente.direccion = request.POST.get('direccion', '').strip()
        cliente.ciudad = request.POST.get('ciudad', '').strip()
        cliente.provincia = request.POST.get('provincia', '').strip()
        cliente.referencia = request.POST.get('referencia', '').strip()
        cliente.tipo_cliente = request.POST.get('tipo_cliente', '').strip()

        cliente.save()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect('listarClientes')

    return redirect('listarClientes')
