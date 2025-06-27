from django.shortcuts import render

# Create your views here.
def inicioClientes(request):
    return render(request, 'Clientes/inicioClientes.html')
