from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from app.models import unidad_medida, Producto
import re


def unidades(request):
    lista = unidad_medida.objects.all()
    return render(request, 'Unidad_medida/unidades.html', {'unidades': lista})


def crear_unidad(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_unidad', '').strip()
        abreviatura = request.POST.get('abreviatura', '').strip()
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        elif len(nombre) < 2:
            messages.error(request, 'El nombre debe tener al menos 2 letras.')
        elif len(nombre) > 100:
            messages.error(request, 'El nombre no puede superar 100 letras.')
        elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.')
        elif unidad_medida.objects.filter(nombre_unidad__iexact=nombre).exists():
            messages.error(request, f'Ya existe una unidad llamada "{nombre}".')
        else:
            unidad_medida.objects.create(nombre_unidad=nombre, abreviatura=abreviatura or '-')
            messages.success(request, f'Unidad "{nombre}" creada exitosamente.')
            return redirect(reverse('productos') + '?abrir_modal=1')
    return redirect('unidades')


def eliminar_unidad(request, id):
    unidad = get_object_or_404(unidad_medida, idUnidad=id)
    if request.method == 'POST':
        if Producto.objects.filter(idUnidad=unidad).exists():
            messages.error(request, f'No se puede eliminar "{unidad.nombre_unidad}": tiene productos asociados.')
        else:
            nombre = unidad.nombre_unidad
            unidad.delete()
            messages.success(request, f'Unidad "{nombre}" eliminada.')
    return redirect('unidades')