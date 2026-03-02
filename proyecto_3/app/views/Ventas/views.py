"""Vistas para gestión de ventas"""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from ...models import Venta, DetalleVenta, Producto, Cliente


@login_required
def ventas(request):
    """Lista de ventas con estadísticas"""
    hoy = timezone.now().date()

    ventas_hoy = Venta.objects.filter(
        fecha__date=hoy
    ).aggregate(total=Sum('total'))['total'] or 0

    total_mes = Venta.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month
    ).aggregate(total=Sum('total'))['total'] or 0

    buscar = request.GET.get('buscar', '').strip()
    lista_ventas = Venta.objects.prefetch_related('detalles').all()
    if buscar:
        lista_ventas = lista_ventas.filter(cliente__icontains=buscar)

    return render(request, "Ventas/Ventas.html", {
        'ventas': lista_ventas,
        'ventas_hoy': ventas_hoy,
        'total_mes': total_mes,
        'total_ventas': Venta.objects.count(),
        'clientes': Cliente.objects.filter(estado='Activo'),
        'productos': Producto.objects.all(),
    })


@login_required
def crear_venta(request):
    """Crear una nueva venta"""
    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente', '').strip()
        estado = request.POST.get('estado', 'Pendiente')
        productos_json_str = request.POST.get('productos', '[]')

        if not cliente_nombre or len(cliente_nombre) < 3:
            messages.error(request, 'El nombre del cliente debe tener al menos 3 caracteres.')
            return redirect('ventas')

        try:
            productos_lista = json.loads(productos_json_str)
        except (json.JSONDecodeError, ValueError):
            productos_lista = []

        if not productos_lista:
            messages.error(request, 'Debe agregar al menos un producto.')
            return redirect('ventas')

        try:
            total = sum(float(p.get('precio', 0)) * int(p.get('cantidad', 1)) for p in productos_lista)
            venta = Venta.objects.create(
                cliente=cliente_nombre,
                estado=estado,
                total=total,
            )
            for p in productos_lista:
                DetalleVenta.objects.create(
                    venta=venta,
                    producto_nombre=p['nombre'],
                    precio=p['precio'],
                    cantidad=p['cantidad'],
                )
            messages.success(request, f'Venta #{venta.id} creada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear la venta: {str(e)}')

    return redirect('ventas')


@login_required
def detalle_venta(request, id):
    """Ver detalle de una venta"""
    venta = get_object_or_404(Venta, id=id)
    return render(request, 'Ventas/detalle_venta.html', {'venta': venta})


@login_required
def editar_venta(request, id):
    """Editar una venta existente (cliente y estado)"""
    venta = get_object_or_404(Venta, id=id)

    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente', '').strip()
        estado = request.POST.get('estado', 'Pendiente')

        if not cliente_nombre:
            messages.error(request, 'El nombre del cliente es obligatorio.')
            return redirect('ventas')

        try:
            venta.cliente = cliente_nombre
            venta.estado = estado
            venta.save()
            messages.success(request, f'Venta #{venta.id} actualizada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')

    return redirect('ventas')


@login_required
def completar_venta(request, id):
    """Marcar una venta como completada"""
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=id)
        venta.estado = 'Completada'
        venta.save()
        messages.success(request, f'Venta #{venta.id} marcada como completada.')
    return redirect('ventas')


@login_required
def eliminar_venta(request, id):
    """Eliminar una venta"""
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=id)
        venta_id = venta.id
        venta.delete()
        messages.success(request, f'Venta #{venta_id} eliminada exitosamente.')
    return redirect('ventas')


@login_required
def estadisticas_ventas(request):
    """Estadísticas de ventas en JSON"""
    hoy = timezone.now().date()
    ventas_hoy = Venta.objects.filter(fecha__date=hoy).aggregate(total=Sum('total'))['total'] or 0
    total_mes = Venta.objects.filter(fecha__year=hoy.year, fecha__month=hoy.month).aggregate(total=Sum('total'))['total'] or 0
    total_ventas = Venta.objects.count()
    from django.http import JsonResponse
    return JsonResponse({
        'ventas_hoy': float(ventas_hoy),
        'total_mes': float(total_mes),
        'total_ventas': total_ventas,
    })
