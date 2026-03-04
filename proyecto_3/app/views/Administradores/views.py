"""Vistas para gestión de administradores"""
from django.shortcuts import render, redirect
from django.contrib import messages
from app.decorators import admin_login_required
from ...models import Administrador
from ...forms import AdministradorRegistroForm


@admin_login_required
def admin_registro(request):
    """Vista de registro de administradores"""
    if request.method == 'POST':
        form = AdministradorRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('inicio')
    else:
        form = AdministradorRegistroForm()

    return render(request, 'Login/registro.html', {'form': form})
