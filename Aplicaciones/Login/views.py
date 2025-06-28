from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

def vista_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()  # Puede ser username o email
        password = request.POST.get('password', '')

        # Buscar el usuario por username o email
        try:
            user_obj = User.objects.get(email=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier  # Puede que sea el username directamente

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.username}!')
            return redirect('/Clientes/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')

    return render(request, 'Login/login.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not email or not password:
            messages.warning(request, 'Todos los campos son obligatorios.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')

    return render(request, 'Login/registro.html')

@login_required
def perfil(request):
    return render(request, 'Login/perfil.html', {
        'usuario': request.user
    })

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()

        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil')
        else:
            messages.warning(request, "Todos los campos son obligatorios.")

    return render(request, 'Login/editarperfil.html', { 'usuario': request.user })