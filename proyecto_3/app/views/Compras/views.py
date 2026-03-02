"""Vistas para gestión de compras"""
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...models import Compra, Proveedor, Producto, Administrador


def _get_or_create_admin():
    """Obtiene el primer administrador disponible, o lo crea desde auth_user."""
    from django.contrib.auth.models import User

    admin = Administrador.objects.first()
    if not admin:
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if user:
            admin = Administrador.objects.create(
                nombre=user.get_full_name() or user.username,
                usuario=user.username,
                contrasena=user.password,
                email=user.email or f'{user.username}@admin.com',
                fechaRegistro=date.today(),
            )
    return admin


@login_required
def compras(request):
    """Lista de compras"""
    lista_compras = Compra.objects.select_related(
        'Administrador', 'Producto', 'Proveedor'
    ).all().order_by('-fecha')

    return render(request, 'Compras/Compras.html', {
        'compras': lista_compras,
        'proveedores': Proveedor.objects.all(),
        'productos': Producto.objects.all(),
        'administradores': Administrador.objects.all(),
    })


@login_required
def crear_compra(request):
    """Crear una nueva compra"""
    if request.method == 'POST':
        try:
            fecha_str = request.POST.get('fecha', '').strip()
            estado_str = request.POST.get('estado', 'False').strip()
            producto_id = request.POST.get('producto_id', '').strip()
            proveedor_id = request.POST.get('proveedor_id', '').strip()

            if not fecha_str or not producto_id or not proveedor_id:
                messages.error(request, 'Fecha, producto y proveedor son obligatorios.')
                return redirect('compras')

            admin = _get_or_create_admin()
            if not admin:
                messages.error(request, 'No hay administradores registrados en el sistema.')
                return redirect('compras')

            Compra.objects.create(
                fecha=fecha_str,
                estado=estado_str == 'True' or estado_str == '1',
                Administrador=admin,
                Producto_id=int(producto_id),
                Proveedor_id=int(proveedor_id),
            )
            messages.success(request, 'Compra registrada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear la compra: {str(e)}')

    return redirect('compras')


@login_required
def editar_compra(request, id):
    """Editar una compra existente"""
    compra = get_object_or_404(Compra, id=id)

    if request.method == 'POST':
        try:
            fecha_str = request.POST.get('fecha', '').strip()
            estado_str = request.POST.get('estado', 'False').strip()
            producto_id = request.POST.get('producto_id', '').strip()
            proveedor_id = request.POST.get('proveedor_id', '').strip()

            if not fecha_str or not producto_id or not proveedor_id:
                messages.error(request, 'Fecha, producto y proveedor son obligatorios.')
                return redirect('compras')

            admin = _get_or_create_admin()
            if not admin:
                messages.error(request, 'No hay administradores registrados en el sistema.')
                return redirect('compras')

            compra.fecha = fecha_str
            compra.estado = estado_str == 'True' or estado_str == '1'
            compra.Administrador = admin
            compra.Producto_id = int(producto_id)
            compra.Proveedor_id = int(proveedor_id)
            compra.save()

            messages.success(request, 'Compra actualizada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')

    return redirect('compras')


@login_required
def eliminar_compra(request, id):
    """Eliminar una compra"""
    compra = get_object_or_404(Compra, id=id)

    if request.method == 'POST':
        try:
            compra.delete()
            messages.success(request, 'Compra eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')

    return redirect('compras')


@login_required
def compras_json(request):
    """Lista de compras en formato JSON"""
    from django.http import JsonResponse
    lista = []
    for c in Compra.objects.select_related('Administrador', 'Producto', 'Proveedor').all().order_by('-fecha'):
        lista.append({
            'id': c.id,
            'fecha': str(c.fecha),
            'estado': c.estado,
            'administrador': c.Administrador.nombre if c.Administrador else '',
            'administrador_id': c.Administrador_id,
            'producto': c.Producto.nombre if c.Producto else '',
            'producto_id': c.Producto_id,
            'proveedor': c.Proveedor.nombre if c.Proveedor else '',
            'proveedor_id': c.Proveedor_id,
        })
    return JsonResponse({'compras': lista})
