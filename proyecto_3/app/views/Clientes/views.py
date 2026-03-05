"""Vistas para gestión de clientes"""
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.decorators import admin_login_required
from ...models import Cliente

PATRON_EMAIL = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'


def _validar_cliente(nombre, documento, telefono, email, direccion, estado, cliente_id=None):
    """Valida los datos del cliente. Retorna lista de errores."""
    errores = []

    # Nombre
    if not nombre or len(nombre) < 3:
        errores.append('El nombre debe tener al menos 3 caracteres.')
    elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
        errores.append('El nombre solo puede contener letras y espacios.')

    # Documento: máximo 12 según modelo, mínimo 6
    if not documento:
        errores.append('El documento es obligatorio.')
    elif not documento.isdigit():
        errores.append('El documento solo puede contener números.')
    elif len(documento) < 6 or len(documento) > 12:
        errores.append('El documento debe tener entre 6 y 12 dígitos.')
    else:
        qs = Cliente.objects.filter(documento=documento)
        if cliente_id:
            qs = qs.exclude(id=cliente_id)
        if qs.exists():
            errores.append('Ya existe un cliente con ese documento.')

    # Teléfono
    if not telefono:
        errores.append('El teléfono es obligatorio.')
    elif not telefono.isdigit():
        errores.append('El teléfono solo puede contener números.')
    elif len(telefono) < 7 or len(telefono) > 15:
        errores.append('El teléfono debe tener entre 7 y 15 dígitos.')

    # Email
    if not email:
        errores.append('El email es obligatorio.')
    elif not re.match(PATRON_EMAIL, email):
        errores.append('El email no tiene un formato válido (ejemplo: cliente@empresa.com).')
    else:
        qs = Cliente.objects.filter(email=email)
        if cliente_id:
            qs = qs.exclude(id=cliente_id)
        if qs.exists():
            errores.append('Ya existe un cliente con ese email.')

    # Dirección
    if not direccion or len(direccion) < 5:
        errores.append('La dirección debe tener al menos 5 caracteres.')

    # Estado: el modelo usa minúsculas ('activo', 'inactivo') ✅
    if estado not in ['activo', 'inactivo']:
        errores.append('Debe seleccionar un estado válido.')

    return errores


@admin_login_required
def clientes(request):
    """Lista de clientes con filtros"""
    clientes_list = Cliente.objects.all()

    busqueda = request.GET.get('busqueda', '').strip()
    if busqueda:
        clientes_list = clientes_list.filter(nombre__icontains=busqueda)

    estado = request.GET.get('estado', '').strip()
    if estado:
        clientes_list = clientes_list.filter(estado=estado)

    return render(request, "Clientes/clientes.html", {
        'clientes': clientes_list
    })


@admin_login_required
def crear_cliente(request):
    """Crear un nuevo cliente"""
    if request.method == 'POST':
        nombre    = request.POST.get('nombre', '').strip()
        documento = request.POST.get('documento', '').strip()
        telefono  = request.POST.get('telefono', '').strip()
        email     = request.POST.get('email', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        estado    = request.POST.get('estado', '').strip()

        errores = _validar_cliente(nombre, documento, telefono, email, direccion, estado)

        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            try:
                Cliente.objects.create(
                    nombre=nombre,
                    documento=documento,
                    telefono=telefono,
                    email=email,
                    direccion=direccion,
                    estado=estado,
                )
                messages.success(request, f'Cliente "{nombre}" creado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al crear el cliente: {str(e)}')

    return redirect('clientes')


@admin_login_required
def editar_cliente(request, id):
    """Editar un cliente existente"""
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        nombre    = request.POST.get('nombre', '').strip()
        documento = request.POST.get('documento', '').strip()
        telefono  = request.POST.get('telefono', '').strip()
        email     = request.POST.get('email', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        estado    = request.POST.get('estado', '').strip()

        errores = _validar_cliente(nombre, documento, telefono, email, direccion, estado, cliente_id=id)

        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            try:
                cliente.nombre    = nombre
                cliente.documento = documento
                cliente.telefono  = telefono
                cliente.email     = email
                cliente.direccion = direccion
                cliente.estado    = estado
                cliente.save()
                messages.success(request, f'Cliente "{cliente.nombre}" actualizado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')

    return redirect('clientes')


@admin_login_required
def eliminar_cliente(request, id):
    """Eliminar un cliente"""
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        try:
            nombre = cliente.nombre
            cliente.delete()
            messages.success(request, f'Cliente "{nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')

    return redirect('clientes')


@admin_login_required
def clientes_json(request):
    """Lista de clientes en formato JSON"""
    from django.http import JsonResponse
    lista = list(Cliente.objects.all().values(
        'id', 'nombre', 'documento', 'telefono', 'email', 'direccion', 'estado'
    ))
    return JsonResponse({'clientes': lista})