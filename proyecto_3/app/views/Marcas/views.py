from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.models import Marca, Producto
import re


@login_required
def marcas(request):
    lista = Marca.objects.all()
    return render(request, 'Marcas/marcas.html', {'marcas': lista})


@login_required
def crear_marca(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreMarca', '').strip()
        next_url = request.POST.get('next', 'productos')
        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
        elif len(nombre) < 2:
            messages.error(request, 'El nombre debe tener al menos 2 letras.')
        elif len(nombre) > 100:
            messages.error(request, 'El nombre no puede superar 100 letras.')
        elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.')
        elif Marca.objects.filter(nombreMarca__iexact=nombre).exists():
            messages.error(request, f'Ya existe una marca llamada "{nombre}".')
        else:
            Marca.objects.create(nombreMarca=nombre)
            messages.success(request, f'Marca "{nombre}" creada exitosamente.')
            return redirect(reverse('productos') + '?abrir_modal=1')
    return redirect('marcas')




@login_required
def eliminar_marca(request, id):
    marca = get_object_or_404(Marca, idMarca=id)
    if request.method == 'POST':
        if Producto.objects.filter(idMarca=marca).exists():
            messages.error(request, f'No se puede eliminar "{marca.nombreMarca}": tiene productos asociados.')
        else:
            nombre = marca.nombreMarca
            marca.delete()
            messages.success(request, f'Marca "{nombre}" eliminada.')
    return redirect('marcas')