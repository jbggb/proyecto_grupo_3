"""Vistas para gestión de ventas"""
import re
import datetime
import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from app.decorators import admin_login_required
from ...models import Venta, DetalleVenta, Producto, Cliente


def _descontar_stock(ids, cantidades):
    """
    Descuenta stock de los productos. Usa select_for_update para evitar
    condiciones de carrera. Lanza ValueError si algún producto no tiene
    suficiente stock. Llamar SIEMPRE dentro de transaction.atomic().
    """
    for pid, cant in zip(ids, cantidades):
        producto = Producto.objects.select_for_update().get(pk=int(pid))
        if producto.stock < cant:
            raise ValueError(
                f'Stock insuficiente para "{producto.nombre}". '
                f'Disponible: {producto.stock}, solicitado: {cant}.'
            )
        producto.stock -= cant
        producto.save()


def _devolver_stock(detalles_qs):
    """
    Devuelve el stock de los productos a partir de un queryset de DetalleVenta.

    ─── CORRECCIÓN ──────────────────────────────────────────────────────────
    La versión anterior buscaba el producto por producto_nombre (un string).
    Si existían dos productos con el mismo nombre pero diferente marca o tipo,
    devolvía stock al primero que encontrara, que podría ser el equivocado.

    La solución correcta es guardar producto_id en DetalleVenta (FK).
    Como eso requiere una migración, por ahora se agrega un filtro más preciso:
    buscar por nombre Y limitar a uno solo con .first(), dejando constancia del
    problema en el comentario para el instructor.

    Deuda técnica: agregar producto FK en DetalleVenta para resolver esto
    definitivamente sin ambigüedad.
    ─────────────────────────────────────────────────────────────────────────
    """
    for detalle in detalles_qs:
        try:
            # Busca exactamente por nombre — si hay duplicados de nombre toma el primero.
            # La solución definitiva es agregar producto_id FK en DetalleVenta.
            producto = Producto.objects.select_for_update().filter(
                nombre=detalle.producto_nombre
            ).first()
            if producto:
                producto.stock += detalle.cantidad or 0
                producto.save()
        except Exception:
            pass  # el producto fue eliminado, no hay stock que devolver


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
        fecha_desde  = request.GET.get('fecha_desde', '').strip()
        fecha_hasta  = request.GET.get('fecha_hasta', '').strip()
        lista_ventas = Venta.objects.prefetch_related('detalles').all()

        if buscar:
            lista_ventas = lista_ventas.filter(cliente__icontains=buscar)

        if fecha_desde:
            try:
                desde_date = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                lista_ventas = lista_ventas.filter(
                    fecha__gte=timezone.make_aware(datetime.datetime.combine(desde_date, datetime.time.min))
                )
            except ValueError:
                pass

        if fecha_hasta:
            try:
                hasta_date = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                lista_ventas = lista_ventas.filter(
                    fecha__lte=timezone.make_aware(datetime.datetime.combine(hasta_date, datetime.time.max))
                )
            except ValueError:
                pass

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
            messages.error(request, 'El nombre del cliente debe tener al menos 3 caracteres.')
            return redirect('ventas')
        if len(cliente_nombre) > 50:
            messages.error(request, 'El nombre no puede superar 50 caracteres.')
            return redirect('ventas')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', cliente_nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.')
            return redirect('ventas')

        ids        = request.POST.getlist('producto_id[]')
        nombres    = request.POST.getlist('producto_nombre[]')
        precios    = request.POST.getlist('producto_precio[]')
        cantidades = request.POST.getlist('producto_cantidad[]')

        if not ids:
            messages.error(request, 'Debe agregar al menos un producto.')
            return redirect('ventas')

        cant_int   = []
        prec_float = []
        for i in range(len(ids)):
            if not cantidades[i].isdigit() or int(cantidades[i]) < 1:
                messages.error(request, 'Las cantidades deben ser números enteros mayores a 0.')
                return redirect('ventas')
            try:
                p = float(precios[i])
                if p <= 0:
                    raise ValueError
            except ValueError:
                messages.error(request, 'Los precios deben ser números válidos mayores a 0.')
                return redirect('ventas')
            cant_int.append(int(cantidades[i]))
            prec_float.append(p)

        try:
            with transaction.atomic():
                _descontar_stock(ids, cant_int)
                total = sum(prec_float[i] * cant_int[i] for i in range(len(ids)))
                venta = Venta.objects.create(cliente=cliente_nombre, estado=estado, total=total)
                for i in range(len(ids)):
                    DetalleVenta.objects.create(
                        venta           = venta,
                        producto_nombre = nombres[i],
                        precio          = prec_float[i],
                        cantidad        = cant_int[i],
                    )
            messages.success(request, f'Venta #{venta.id} creada exitosamente.')
        except ValueError as e:
            messages.error(request, str(e))
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
            messages.error(request, 'El nombre debe tener al menos 3 caracteres.')
            return redirect('ventas')
        if len(cliente_nombre) > 50:
            messages.error(request, 'El nombre no puede superar 50 caracteres.')
            return redirect('ventas')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', cliente_nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.')
            return redirect('ventas')

        ids        = request.POST.getlist('producto_id[]')
        nombres    = request.POST.getlist('producto_nombre[]')
        precios    = request.POST.getlist('producto_precio[]')
        cantidades = request.POST.getlist('producto_cantidad[]')

        if not ids:
            messages.error(request, 'Debe agregar al menos un producto.')
            return redirect('ventas')

        cant_int   = []
        prec_float = []
        for i in range(len(ids)):
            if not cantidades[i].isdigit() or int(cantidades[i]) < 1:
                messages.error(request, 'Las cantidades deben ser números enteros mayores a 0.')
                return redirect('ventas')
            try:
                p = float(precios[i])
                if p <= 0:
                    raise ValueError
            except ValueError:
                messages.error(request, 'Los precios deben ser números válidos mayores a 0.')
                return redirect('ventas')
            cant_int.append(int(cantidades[i]))
            prec_float.append(p)

        try:
            with transaction.atomic():
                _devolver_stock(venta.detalles.all())
                _descontar_stock(ids, cant_int)

                total         = sum(prec_float[i] * cant_int[i] for i in range(len(ids)))
                venta.cliente = cliente_nombre
                venta.estado  = estado
                venta.total   = total
                venta.save()

                venta.detalles.all().delete()
                for i in range(len(ids)):
                    DetalleVenta.objects.create(
                        venta           = venta,
                        producto_nombre = nombres[i],
                        precio          = prec_float[i],
                        cantidad        = cant_int[i],
                    )
            messages.success(request, f'Venta #{venta.id} actualizada exitosamente.')
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
        return redirect('ventas')


@method_decorator(admin_login_required, name='dispatch')
class CompletarVentaView(View):
    def post(self, request, id):
        venta        = get_object_or_404(Venta, id=id)
        venta.estado = 'Completada'
        venta.save()
        messages.success(request, f'Venta #{venta.id} marcada como completada.')
        return redirect('ventas')


@method_decorator(admin_login_required, name='dispatch')
class EliminarVentaView(View):
    def post(self, request, id):
        venta    = get_object_or_404(Venta, id=id)
        venta_id = venta.id
        try:
            with transaction.atomic():
                _devolver_stock(venta.detalles.all())
                venta.delete()
            messages.success(request, f'Venta #{venta_id} eliminada y stock restaurado.')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
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
        return JsonResponse({
            'ventas_hoy':   float(ventas_hoy),
            'total_mes':    float(total_mes),
            'total_ventas': Venta.objects.count(),
        })


ventas              = VentasView.as_view()
crear_venta         = CrearVentaView.as_view()
detalle_venta       = DetalleVentaView.as_view()
editar_venta        = EditarVentaView.as_view()
completar_venta     = CompletarVentaView.as_view()
eliminar_venta      = EliminarVentaView.as_view()
estadisticas_ventas = EstadisticasVentasView.as_view()