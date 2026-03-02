"""Vistas para gestión de unidades de medida"""
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...models import unidad_medida, Producto


@login_required
def crear_unidad(request):
    """Crear una nueva unidad de medida"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre_unidad', '').strip()
        abrev = request.POST.get('abreviatura', '-').strip() or '-'

        if not nombre:
            messages.error(request, 'El nombre de la unidad es obligatorio.')
        else:
            unidad_medida.objects.create(nombre_unidad=nombre, abreviatura=abrev)
            messages.success(request, f'Unidad "{nombre}" creada exitosamente.')

    return redirect(request.POST.get('next', 'productos'))


@login_required
def eliminar_unidad(request, id):
    """Eliminar una unidad de medida"""
    if request.method == 'POST':
        unidad = get_object_or_404(unidad_medida, idUnidad=id)

        if Producto.objects.filter(idUnidad=unidad).exists():
            messages.error(request, f'No se puede eliminar la unidad "{unidad.nombre_unidad}": tiene productos asociados.')
        else:
            nombre = unidad.nombre_unidad
            unidad.delete()
            messages.success(request, f'Unidad "{nombre}" eliminada exitosamente.')

    return redirect(request.POST.get('next', 'productos'))
