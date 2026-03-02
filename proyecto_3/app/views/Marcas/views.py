"""Vistas para gestión de marcas"""
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...models import Marca, Producto


@login_required
def crear_marca(request):
    """Crear una nueva marca"""
    if request.method == 'POST':
        nombre = request.POST.get('nombreMarca', '').strip()

        if not nombre:
            messages.error(request, 'El nombre de la marca es obligatorio.')
        elif Marca.objects.filter(nombreMarca__iexact=nombre).exists():
            messages.error(request, f'Ya existe una marca con el nombre "{nombre}".')
        else:
            Marca.objects.create(nombreMarca=nombre)
            messages.success(request, f'Marca "{nombre}" creada exitosamente.')

    return redirect(request.POST.get('next', 'productos'))


@login_required
def eliminar_marca(request, id):
    """Eliminar una marca"""
    if request.method == 'POST':
        marca = get_object_or_404(Marca, idMarca=id)

        if Producto.objects.filter(idMarca=marca).exists():
            messages.error(request, f'No se puede eliminar la marca "{marca.nombreMarca}": tiene productos asociados.')
        else:
            nombre = marca.nombreMarca
            marca.delete()
            messages.success(request, f'Marca "{nombre}" eliminada exitosamente.')

    return redirect(request.POST.get('next', 'productos'))
