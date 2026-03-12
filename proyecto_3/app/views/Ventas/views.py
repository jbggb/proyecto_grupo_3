"""Vistas para gestión de ventas"""
import re
import datetime
import calendar
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse
from app.decorators import admin_login_required
from ...models import Venta, DetalleVenta, Producto, Cliente


def rango_dia(fecha):
    inicio = timezone.make_aware(datetime.datetime.combine(fecha, datetime.time.min))
    fin    = timezone.make_aware(datetime.datetime.combine(fecha, datetime.time.max))
    return inicio, fin


@method_decorator(admin_login_required, name='dispatch')
class VentasView(View):
    def get(self, request):
        ahora = timezone.localtime(timezone.now())
        hoy   = ahora.date()

        inicio_hoy, fin_hoy = rango_dia(hoy)
        ventas_hoy = Venta.objects.filter(fecha__range=(inicio_hoy, fin_hoy)).aggregate(total=Sum('total'))['total'] or 0

        inicio_mes = timezone.make_aware(datetime.datetime(hoy.year, hoy.month, 1))
        total_mes  = Venta.objects.filter(fecha__gte=inicio_mes).aggregate(total=Sum('total'))['total'] or 0

        buscar       = request.GET.get('buscar', '').strip()
        fecha_filtro = request.GET.get('fecha_filtro', '').strip()
        lista_ventas = Venta.objects.prefetch_related('detalles').all()

        if buscar:
            lista_ventas = lista_ventas.filter(cliente__icontains=buscar)

        if fecha_filtro == 'hoy':
            lista_ventas = lista_ventas.filter(fecha__range=rango_dia(hoy))
        elif fecha_filtro == 'ayer':
            lista_ventas = lista_ventas.filter(fecha__range=rango_dia(hoy - datetime.timedelta(days=1)))
        elif fecha_filtro == 'semana':
            inicio = timezone.make_aware(datetime.datetime.combine(hoy - datetime.timedelta(days=hoy.weekday()), datetime.time.min))
            lista_ventas = lista_ventas.filter(fecha__gte=inicio)
        elif fecha_filtro == 'semana_pasada':
            inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
            inicio_sp = inicio_semana - datetime.timedelta(days=7)
            fin_sp    = inicio_semana - datetime.timedelta(days=1)
            lista_ventas = lista_ventas.filter(fecha__range=(
                timezone.make_aware(datetime.datetime.combine(inicio_sp, datetime.time.min)),
                timezone.make_aware(datetime.datetime.combine(fin_sp, datetime.time.max)),
            ))
        elif fecha_filtro == 'mes':
            lista_ventas = lista_ventas.filter(fecha__gte=timezone.make_aware(datetime.datetime(hoy.year, hoy.month, 1)))
        elif fecha_filtro == 'mes_pasado':
            anio, mes = (hoy.year - 1, 12) if hoy.month == 1 else (hoy.year, hoy.month - 1)
            ultimo_dia = calendar.monthrange(anio, mes)[1]
            lista_ventas = lista_ventas.filter(fecha__range=(
                timezone.make_aware(datetime.datetime(anio, mes, 1)),
                timezone.make_aware(datetime.datetime(anio, mes, ultimo_dia, 23, 59, 59)),
            ))
        elif fecha_filtro == 'anio':
            lista_ventas = lista_ventas.filter(fecha__gte=timezone.make_aware(datetime.datetime(hoy.year, 1, 1)))

        return render(request, 'Ventas/Ventas.html', {
            'ventas':       lista_ventas,
            'ventas_hoy':   ventas_hoy,
            'total_mes':    total_mes,
            'total_ventas': Venta.objects.count(),
            'clientes':     Cliente.objects.filter(estado='activo'),
            'productos':    Producto.objects.all(),
        })


@method_decorator(admin_login_required, name='dispatch')
class CrearVentaView(View):
    def post(self, request):
        cliente_nombre = request.POST.get('cliente', '').strip()
        estado         = request.POST.get('estado', 'Pendiente')

        if not cliente_nombre or len(cliente_nombre) < 3:
            messages.error(request, 'El nombre del cliente debe tener al menos 3 caracteres.'); return redirect('ventas')
        if len(cliente_nombre) > 50:
            messages.error(request, 'El nombre no puede superar 50 caracteres.'); return redirect('ventas')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', cliente_nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.'); return redirect('ventas')

        ids        = request.POST.getlist('producto_id[]')
        nombres    = request.POST.getlist('producto_nombre[]')
        precios    = request.POST.getlist('producto_precio[]')
        cantidades = request.POST.getlist('producto_cantidad[]')

        if not ids:
            messages.error(request, 'Debe agregar al menos un producto.'); return redirect('ventas')

        try:
            for i in range(len(ids)):
                if not cantidades[i].isdigit() or int(cantidades[i]) < 1:
                    messages.error(request, 'Las cantidades deben ser números enteros mayores a 0.'); return redirect('ventas')
                try:
                    if float(precios[i]) <= 0:
                        messages.error(request, 'Los precios deben ser mayores a 0.'); return redirect('ventas')
                except ValueError:
                    messages.error(request, 'Los precios deben ser números válidos.'); return redirect('ventas')
            total = sum(float(precios[i]) * int(cantidades[i]) for i in range(len(ids)))
            venta = Venta.objects.create(cliente=cliente_nombre, estado=estado, total=total)
            for i in range(len(ids)):
                DetalleVenta.objects.create(venta=venta, producto_nombre=nombres[i],
                                            precio=float(precios[i]), cantidad=int(cantidades[i]))
            messages.success(request, f'Venta #{venta.id} creada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear la venta: {str(e)}')
        return redirect('ventas')


@method_decorator(admin_login_required, name='dispatch')
class DetalleVentaView(View):
    def get(self, request, id):
        return render(request, 'Ventas/detalle_venta.html', {'venta': get_object_or_404(Venta, id=id)})


@method_decorator(admin_login_required, name='dispatch')
class EditarVentaView(View):
    def post(self, request, id):
        venta          = get_object_or_404(Venta, id=id)
        cliente_nombre = request.POST.get('cliente', '').strip()
        estado         = request.POST.get('estado', 'Pendiente')

        if not cliente_nombre or len(cliente_nombre) < 3:
            messages.error(request, 'El nombre debe tener al menos 3 caracteres.'); return redirect('ventas')
        if len(cliente_nombre) > 50:
            messages.error(request, 'El nombre no puede superar 50 caracteres.'); return redirect('ventas')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', cliente_nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.'); return redirect('ventas')

        try:
            venta.cliente = cliente_nombre; venta.estado = estado; venta.save()
            messages.success(request, f'Venta #{venta.id} actualizada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
        return redirect('ventas')


@method_decorator(admin_login_required, name='dispatch')
class CompletarVentaView(View):
    def post(self, request, id):
        venta = get_object_or_404(Venta, id=id)
        venta.estado = 'Completada'; venta.save()
        messages.success(request, f'Venta #{venta.id} marcada como completada.')
        return redirect('ventas')


@method_decorator(admin_login_required, name='dispatch')
class EliminarVentaView(View):
    def post(self, request, id):
        venta = get_object_or_404(Venta, id=id)
        venta_id = venta.id; venta.delete()
        messages.success(request, f'Venta #{venta_id} eliminada exitosamente.')
        return redirect('ventas')


@method_decorator(admin_login_required, name='dispatch')
class EstadisticasVentasView(View):
    def get(self, request):
        ahora = timezone.localtime(timezone.now())
        hoy   = ahora.date()
        inicio_hoy, fin_hoy = rango_dia(hoy)
        ventas_hoy = Venta.objects.filter(fecha__range=(inicio_hoy, fin_hoy)).aggregate(total=Sum('total'))['total'] or 0
        inicio_mes = timezone.make_aware(datetime.datetime(hoy.year, hoy.month, 1))
        total_mes  = Venta.objects.filter(fecha__gte=inicio_mes).aggregate(total=Sum('total'))['total'] or 0
        return JsonResponse({'ventas_hoy': float(ventas_hoy), 'total_mes': float(total_mes), 'total_ventas': Venta.objects.count()})


ventas              = VentasView.as_view()
crear_venta         = CrearVentaView.as_view()
detalle_venta       = DetalleVentaView.as_view()
editar_venta        = EditarVentaView.as_view()
completar_venta     = CompletarVentaView.as_view()
eliminar_venta      = EliminarVentaView.as_view()
estadisticas_ventas = EstadisticasVentasView.as_view()
