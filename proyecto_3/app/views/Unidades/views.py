"""Vistas para gestión de unidades de medida"""
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.urls import reverse
from app.decorators import admin_login_required
from app.models import unidad_medida, Producto


@method_decorator(admin_login_required, name='dispatch')
class UnidadesView(View):
    def get(self, request):
        return render(request, 'Unidad_medida/unidades.html', {'unidades': unidad_medida.objects.all()})


@method_decorator(admin_login_required, name='dispatch')
class CrearUnidadView(View):
    def post(self, request):
        nombre      = request.POST.get('nombre_unidad', '').strip()
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


@method_decorator(admin_login_required, name='dispatch')
class EliminarUnidadView(View):
    def post(self, request, id):
        unidad = get_object_or_404(unidad_medida, idUnidad=id)
        if Producto.objects.filter(idUnidad=unidad).exists():
            messages.error(request, f'No se puede eliminar "{unidad.nombre_unidad}": tiene productos asociados.')
        else:
            nombre = unidad.nombre_unidad
            unidad.delete()
            messages.success(request, f'Unidad "{nombre}" eliminada.')
        return redirect('unidades')


unidades        = UnidadesView.as_view()
crear_unidad    = CrearUnidadView.as_view()
eliminar_unidad = EliminarUnidadView.as_view()
