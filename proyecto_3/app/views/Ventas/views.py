"""Vistas para gestion de ventas"""
import re
import datetime
import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.decorators import admin_login_required
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse
from ...models import Venta, DetalleVenta, Producto, Cliente


def rango_dia(fecha):
    inicio = timezone.make_aware(datetime.datetime.combine(fecha, datetime.time.min))
    fin = timezone.make_aware(datetime.datetime.combine(fecha, datetime.time.max))
    return inicio, fin


def rango_dia(fecha):
    inicio = timezone.make_aware(datetime.datetime.combine(fecha, datetime.time.min))
    fin = timezone.make_aware(datetime.datetime.combine(fecha, datetime.time.max))
    return inicio, fin


@admin_login_required
def ventas(request):
    ahora = timezone.localtime(timezone.now())
    hoy = ahora.date()

    inicio_hoy, fin_hoy = rango_dia(hoy)
    ventas_hoy = Venta.objects.filter(
        fecha__range=(inicio_hoy, fin_hoy)
    ).aggregate(total=Sum('total'))['total'] or 0

    inicio_mes = timezone.make_aware(datetime.datetime(hoy.year, hoy.month, 1))
    total_mes = Venta.objects.filter(
        fecha__gte=inicio_mes
    ).aggregate(total=Sum('total'))['total'] or 0

    buscar = request.GET.get('buscar', '').strip()
    fecha_filtro = request.GET.get('fecha_filtro', '').strip()
    lista_ventas = Venta.objects.prefetch_related('detalles').all()

    if buscar:
        lista_ventas = lista_ventas.filter(cliente__icontains=buscar)

    if fecha_filtro == 'hoy':
        lista_ventas = lista_ventas.filter(fecha__range=rango_dia(hoy))

    elif fecha_filtro == 'ayer':
        ayer = hoy - datetime.timedelta(days=1)
        lista_ventas = lista_ventas.filter(fecha__range=rango_dia(ayer))

    elif fecha_filtro == 'semana':
        inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
        inicio = timezone.make_aware(
            datetime.datetime.combine(inicio_semana, datetime.time.min)
        )
        lista_ventas = lista_ventas.filter(fecha__gte=inicio)

    elif fecha_filtro == 'semana_pasada':
        inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
        inicio_sp = inicio_semana - datetime.timedelta(days=7)
        fin_sp = inicio_semana - datetime.timedelta(days=1)

        inicio = timezone.make_aware(
            datetime.datetime.combine(inicio_sp, datetime.time.min)
        )
        fin = timezone.make_aware(
            datetime.datetime.combine(fin_sp, datetime.time.max)
        )

        lista_ventas = lista_ventas.filter(fecha__range=(inicio, fin))

    elif fecha_filtro == 'mes':
        inicio = timezone.make_aware(datetime.datetime(hoy.year, hoy.month, 1))
        lista_ventas = lista_ventas.filter(fecha__gte=inicio)

    elif fecha_filtro == 'mes_pasado':
        if hoy.month == 1:
            anio, mes = hoy.year - 1, 12
        else:
            anio, mes = hoy.year, hoy.month - 1

        ultimo_dia = calendar.monthrange(anio, mes)[1]

        inicio = timezone.make_aware(datetime.datetime(anio, mes, 1))
        fin = timezone.make_aware(
            datetime.datetime(anio, mes, ultimo_dia, 23, 59, 59)
        )

        lista_ventas = lista_ventas.filter(fecha__range=(inicio, fin))

    elif fecha_filtro == 'anio':
        inicio = timezone.make_aware(datetime.datetime(hoy.year, 1, 1))
        lista_ventas = lista_ventas.filter(fecha__gte=inicio)

    return render(request, "Ventas/Ventas.html", {
        'ventas': lista_ventas,
        'ventas_hoy': ventas_hoy,
        'total_mes': total_mes,
        'total_ventas': Venta.objects.count(),
        'clientes': Cliente.objects.filter(estado='Activo'),
        'productos': Producto.objects.all(),
    })




@admin_login_required
def crear_venta(request):
    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente', '').strip()
        estado = request.POST.get('estado', 'Pendiente')

        if not cliente_nombre or len(cliente_nombre) < 3:
            messages.error(request, 'El nombre del cliente debe tener al menos 3 caracteres.')
            return redirect('ventas')

        if len(cliente_nombre) > 50:
            messages.error(request, 'El nombre del cliente no puede superar 50 caracteres.')
            return redirect('ventas')

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', cliente_nombre):
            messages.error(request, 'El nombre del cliente solo puede contener letras y espacios.')
            return redirect('ventas')

        ids = request.POST.getlist('producto_id[]')
        nombres = request.POST.getlist('producto_nombre[]')
        precios = request.POST.getlist('producto_precio[]')
        cantidades = request.POST.getlist('producto_cantidad[]')

        if not ids:
            messages.error(request, 'Debe agregar al menos un producto.')
            return redirect('ventas')

        try:
            total = sum(
                float(precios[i]) * int(cantidades[i])
                for i in range(len(ids))
            )

            venta = Venta.objects.create(
                cliente=cliente_nombre,
                estado=estado,
                total=total
            )

            for i in range(len(ids)):
                DetalleVenta.objects.create(
                    venta=venta,
                    producto_nombre=nombres[i],
                    precio=float(precios[i]),
                    cantidad=int(cantidades[i]),
                )

            messages.success(request, f'Venta #{venta.id} creada exitosamente.')

        except Exception as e:
            messages.error(request, f'Error al crear la venta: {str(e)}')

    return redirect('ventas')


@admin_login_required
def detalle_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    return render(request, 'Ventas/detalle_venta.html', {'venta': venta})


@admin_login_required
def editar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)

    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente', '').strip()
        estado = request.POST.get('estado', 'Pendiente')

        if not cliente_nombre or len(cliente_nombre) < 3:
            messages.error(request, 'El nombre del cliente debe tener al menos 3 caracteres.')
            return redirect('ventas')

        if len(cliente_nombre) > 50:
            messages.error(request, 'El nombre no puede superar 50 caracteres.')
            return redirect('ventas')

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', cliente_nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.')
            return redirect('ventas')

        try:
            venta.cliente = cliente_nombre
            venta.estado = estado
            venta.save()
            messages.success(request, f'Venta #{venta.id} actualizada exitosamente.')

        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')

    return redirect('ventas')


@admin_login_required
def completar_venta(request, id):
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=id)
        venta.estado = 'Completada'
        venta.save()
        messages.success(request, f'Venta #{venta.id} marcada como completada.')

    return redirect('ventas')


@admin_login_required
def eliminar_venta(request, id):
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=id)
        venta_id = venta.id
        venta.delete()
        messages.success(request, f'Venta #{venta_id} eliminada exitosamente.')

    return redirect('ventas')


@admin_login_required
def estadisticas_ventas(request):
    ahora = timezone.localtime(timezone.now())
    hoy = ahora.date()

    inicio_hoy, fin_hoy = rango_dia(hoy)
    ventas_hoy = Venta.objects.filter(
        fecha__range=(inicio_hoy, fin_hoy)
    ).aggregate(total=Sum('total'))['total'] or 0

    inicio_mes = timezone.make_aware(datetime.datetime(hoy.year, hoy.month, 1))
    total_mes = Venta.objects.filter(
        fecha__gte=inicio_mes
    ).aggregate(total=Sum('total'))['total'] or 0

    return JsonResponse({
        'ventas_hoy': float(ventas_hoy),
        'total_mes': float(total_mes),
        'total_ventas': Venta.objects.count(),
    })