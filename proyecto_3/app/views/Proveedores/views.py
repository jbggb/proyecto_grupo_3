"""Vistas para gestión de proveedores"""
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.decorators import admin_login_required
from ...models import Proveedor


def _validar_proveedor(nombre, telefono, email, envio, proveedor_id=None):
    """Valida los datos de un proveedor. Retorna lista de errores."""
    errores = []

    # Nombre: solo letras
    if not nombre:
        errores.append('El nombre es obligatorio.')
    elif len(nombre) < 3:
        errores.append('El nombre debe tener al menos 3 caracteres.')
    elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
        errores.append('El nombre solo puede contener letras y espacios.')

    # Teléfono: solo números, entre 7 y 15 dígitos
    if not telefono:
        errores.append('El teléfono es obligatorio.')
    elif not telefono.isdigit():
        errores.append('El teléfono solo puede contener números.')
    elif len(telefono) < 7 or len(telefono) > 15:
        errores.append('El teléfono debe tener entre 7 y 15 dígitos.')

    # Email: formato válido + único
    if not email:
        errores.append('El email es obligatorio.')
    else:
        # ✅ Validar formato de email con regex
        patron_email = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, email):
            errores.append('El email no tiene un formato válido (ejemplo: proveedor@empresa.com).')
        else:
            qs = Proveedor.objects.filter(email=email)
            if proveedor_id:
                qs = qs.exclude(id=proveedor_id)
            if qs.exists():
                errores.append('Ya existe un proveedor con ese email.')

    # Envío: número entero y mínimo 1
    if not envio:
        errores.append('Los días de envío son obligatorios.')
    elif not envio.isdigit():
        errores.append('Los días de envío solo pueden contener números enteros.')
    elif int(envio) < 1:
        errores.append('Los días de envío deben ser al menos 1.')

    return errores


@admin_login_required
def proveedores(request):
    """Lista de proveedores"""
    proveedores_list = Proveedor.objects.all()

    busqueda = request.GET.get('busqueda', '').strip()
    if busqueda:
        proveedores_list = proveedores_list.filter(nombre__icontains=busqueda)

    return render(request, 'Proveedores/proveedores.html', {
        'proveedores': proveedores_list,
        'busqueda': busqueda,
    })


@admin_login_required
def crear_proveedor(request):
    """Crear un nuevo proveedor"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        envio = request.POST.get('envio', '').strip()

        errores = _validar_proveedor(nombre, telefono, email, envio)

        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            try:
                Proveedor.objects.create(
                    nombre=nombre,
                    telefono=telefono,
                    email=email,
                    envio=int(envio),
                )
                messages.success(request, f'Proveedor "{nombre}" creado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al crear el proveedor: {str(e)}')

    return redirect('proveedores')


@admin_login_required
def editar_proveedor(request, id):
    """Editar un proveedor existente"""
    proveedor = get_object_or_404(Proveedor, id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        envio = request.POST.get('envio', '').strip()

        errores = _validar_proveedor(nombre, telefono, email, envio, proveedor_id=id)

        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            try:
                proveedor.nombre = nombre
                proveedor.telefono = telefono
                proveedor.email = email
                proveedor.envio = int(envio)
                proveedor.save()
                messages.success(request, f'Proveedor "{proveedor.nombre}" actualizado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')

    return redirect('proveedores')


@admin_login_required
def eliminar_proveedor(request, id):
    """Eliminar un proveedor"""
    proveedor = get_object_or_404(Proveedor, id=id)

    if request.method == 'POST':
        try:
            nombre = proveedor.nombre
            proveedor.delete()
            messages.success(request, f'Proveedor "{nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')

    return redirect('proveedores')


@admin_login_required
def proveedores_json(request):
    """Lista de proveedores en formato JSON"""
    from django.http import JsonResponse
    lista = list(Proveedor.objects.all().values('id', 'nombre', 'telefono', 'email', 'envio', 'fechaRegistro'))
    return JsonResponse({'proveedores': lista})