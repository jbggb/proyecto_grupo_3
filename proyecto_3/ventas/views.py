from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from app.forms import ventaForm
from .models import venta, detalle_venta


def ventas_view(request):
    ventas = venta.objects.all().order_by('fecha')
    return render(request, 'ventas/ventas.html', {'ventas': ventas})


@require_POST
def crear_venta(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'errores': {'general': 'Datos inválidos'}})

    form = ventaForm(data)
    if form.is_valid():
        nueva = venta.objects.create(
            cliente=form.cleaned_data['cliente'],
            total=data.get('total', 0),
            estado=form.cleaned_data['estado']
        )
        for item in data.get('productos', []):
            detalle_venta.objects.create(
                venta=nueva,
                producto_nombre=item['nombre'],
                cantidad=item['cantidad'],
                precio=item['precio']
            )
        return JsonResponse({'ok': True, 'venta_id': nueva.id})
    else:
        return JsonResponse({'ok': False, 'errores': form.errors})


def detalle_venta_view(request, ventaId):
    v = get_object_or_404(venta, id=ventaId)
    productos = list(v.detalle_venta_set.values('producto_nombre', 'cantidad', 'precio'))
    return JsonResponse({
        'id': v.id,
        'fecha': v.fecha.strftime('%d/%m/%Y %H:%M'),
        'cliente': v.cliente,
        'estado': v.estado,
        'total': float(v.total),
        'productos': [{'nombre': p['producto_nombre'], 'cantidad': p['cantidad'], 'precio': float(p['precio'])} for p in productos]
    })


@require_POST
def completar_venta_view(request, ventaId):
    v = get_object_or_404(venta, id=ventaId)
    v.estado = 'completada'
    v.save()
    return JsonResponse({'ok': True})


@require_POST
def eliminar_venta_view(request, ventaId):
    v = get_object_or_404(venta, id=ventaId)
    v.delete()
    return JsonResponse({'ok': True})


def estadisticas_view(request):
    hoy = timezone.now().date()
    todas = venta.objects.all()
    ventas_hoy = sum(float(v.total) for v in todas if v.fecha.date() == hoy)
    total_mes = sum(float(v.total) for v in todas if v.fecha.month == hoy.month and v.fecha.year == hoy.year)
    return JsonResponse({'ventas_hoy': ventas_hoy, 'total_mes': total_mes, 'total_ventas': todas.count()})