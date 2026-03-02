"""Vistas para gestión de tipos de productos"""
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...models import TipoProductos, Producto


@login_required
def crear_tipo(request):
    """Crear un nuevo tipo de producto"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre_tipo', '').strip()

        if not nombre:
            messages.error(request, 'El nombre del tipo es obligatorio.')
        elif TipoProductos.objects.filter(nombre_tipo__iexact=nombre).exists():
            messages.error(request, f'Ya existe un tipo con el nombre "{nombre}".')
        else:
            TipoProductos.objects.create(nombre_tipo=nombre, descripcion='')
            messages.success(request, f'Tipo "{nombre}" creado exitosamente.')

    return redirect(request.POST.get('next', 'productos'))


@login_required
def eliminar_tipo(request, id):
    """Eliminar un tipo de producto"""
    if request.method == 'POST':
        tipo = get_object_or_404(TipoProductos, idTipo=id)

        if Producto.objects.filter(idTipo=tipo).exists():
            messages.error(request, f'No se puede eliminar el tipo "{tipo.nombre_tipo}": tiene productos asociados.')
        else:
            nombre = tipo.nombre_tipo
            tipo.delete()
            messages.success(request, f'Tipo "{nombre}" eliminado exitosamente.')

    return redirect(request.POST.get('next', 'productos'))
