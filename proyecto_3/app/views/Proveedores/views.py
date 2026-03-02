"""Vistas para gestión de proveedores"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...models import Proveedor


@login_required
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


@login_required
def crear_proveedor(request):
    """Crear un nuevo proveedor"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        envio = request.POST.get('envio', '0').strip()

        if not nombre or not telefono or not email:
            messages.error(request, 'Nombre, teléfono y email son obligatorios.')
        elif Proveedor.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe un proveedor con ese email.')
        else:
            try:
                Proveedor.objects.create(
                    nombre=nombre,
                    telefono=telefono,
                    email=email,
                    envio=int(envio) if envio.isdigit() else 0,
                )
                messages.success(request, f'Proveedor "{nombre}" creado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al crear el proveedor: {str(e)}')

    return redirect('proveedores')


@login_required
def editar_proveedor(request, id):
    """Editar un proveedor existente"""
    proveedor = get_object_or_404(Proveedor, id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        envio = request.POST.get('envio', '0').strip()

        if not nombre or not telefono or not email:
            messages.error(request, 'Nombre, teléfono y email son obligatorios.')
        elif Proveedor.objects.filter(email=email).exclude(id=id).exists():
            messages.error(request, 'Ya existe otro proveedor con ese email.')
        else:
            try:
                proveedor.nombre = nombre
                proveedor.telefono = telefono
                proveedor.email = email
                proveedor.envio = int(envio) if envio.isdigit() else 0
                proveedor.save()
                messages.success(request, f'Proveedor "{proveedor.nombre}" actualizado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')

    return redirect('proveedores')


@login_required
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


@login_required
def proveedores_json(request):
    """Lista de proveedores en formato JSON"""
    from django.http import JsonResponse
    lista = list(Proveedor.objects.all().values('id', 'nombre', 'telefono', 'email', 'envio', 'fechaRegistro'))
    return JsonResponse({'proveedores': lista})
