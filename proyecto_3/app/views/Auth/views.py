"""Vistas de autenticación: login, logout, registro"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from ...models import Administrador
from ...forms import AdministradorRegistroForm


def login_view(request):
    """Vista de inicio de sesión contra tabla Administrador"""
    if request.session.get('admin_id'):
        return redirect('inicio')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            admin = Administrador.objects.get(usuario=username)
            if check_password(password, admin.contrasena):
                request.session['admin_id']      = admin.idAdministrador
                request.session['admin_nombre']  = admin.nombre
                request.session['admin_usuario'] = admin.usuario
                messages.success(request, f'¡Bienvenido, {admin.nombre}!')
                return redirect('inicio')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        except Administrador.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'Login/login.html')


def logout_view(request):
    """Vista de cierre de sesión"""
    request.session.flush()
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')


def registrar_administrador(request):
    """Vista de registro de administradores"""
    if request.method == 'POST':
        form = AdministradorRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Administrador registrado exitosamente!')
            return redirect('login')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = AdministradorRegistroForm()

    return render(request, 'Login/registro.html', {'form': form})