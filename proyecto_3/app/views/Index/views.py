"""Vista principal del sistema — Dashboard con gráficas"""
import json
from datetime import date, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth
from app.decorators import admin_login_required
from app.context_processors import notificaciones
from ...models import Producto, Cliente, Venta, Proveedor, Compra, Reporte, DetalleVenta


STOCK_BAJO = 10   # umbral para alertas


@method_decorator(admin_login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        try:
            # ── Totales ──────────────────────────────────────────────────
            total_productos   = Producto.objects.count()
            total_clientes    = Cliente.objects.count()
            total_ventas      = Venta.objects.count()
            total_proveedores = Proveedor.objects.count()
            total_compras     = Compra.objects.count()
            total_reportes    = Reporte.objects.count()

            # ── Ingresos totales ─────────────────────────────────────────
            ingresos = Venta.objects.aggregate(
                total=Sum(F('cantidad') * F('precio_unitario'))
            )['total'] or 0

            # ── Ventas por mes (últimos 6 meses) ─────────────────────────
            hace_6_meses = date.today() - timedelta(days=180)
            ventas_mes_qs = (
                Venta.objects
                .filter(fechaVenta__gte=hace_6_meses)
                .annotate(mes=TruncMonth('fechaVenta'))
                .values('mes')
                .annotate(total=Count('id'))
                .order_by('mes')
            )
            meses_labels = []
            meses_data   = []
            MESES_ES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
            for v in ventas_mes_qs:
                meses_labels.append(f"{MESES_ES[v['mes'].month - 1]} {v['mes'].year}")
                meses_data.append(v['total'])

            # ── Ingresos por mes (últimos 6 meses) ───────────────────────
            ingresos_mes_qs = (
                Venta.objects
                .filter(fechaVenta__gte=hace_6_meses)
                .annotate(mes=TruncMonth('fechaVenta'))
                .values('mes')
                .annotate(total=Sum(F('cantidad') * F('precio_unitario')))
                .order_by('mes')
            )
            ingresos_data = [float(v['total'] or 0) for v in ingresos_mes_qs]

            # ── Compras por mes (últimos 6 meses) ────────────────────────
            compras_mes_qs = (
                Compra.objects
                .filter(fechaCompra__gte=hace_6_meses)
                .annotate(mes=TruncMonth('fechaCompra'))
                .values('mes')
                .annotate(total=Count('idCompra'))
                .order_by('mes')
            )
            # Alinear con los mismos labels de ventas
            compras_map = {}
            for c in compras_mes_qs:
                key = f"{MESES_ES[c['mes'].month - 1]} {c['mes'].year}"
                compras_map[key] = c['total']
            compras_data = [compras_map.get(l, 0) for l in meses_labels]

            # ── Top 5 productos más vendidos ─────────────────────────────
            try:
                top_productos_qs = (
                    DetalleVenta.objects
                    .values('producto_nombre')
                    .annotate(total=Sum('cantidad'))
                    .order_by('-total')[:5]
                )
                top_productos_labels = [p['producto_nombre'] for p in top_productos_qs]
                top_productos_data   = [p['total'] for p in top_productos_qs]
            except Exception:
                top_productos_labels = []
                top_productos_data   = []

            # ── Productos con stock bajo ─────────────────────────────────
            stock_bajo = (
                Producto.objects
                .filter(stock__lte=STOCK_BAJO)
                .order_by('stock')
                .values('nombre', 'stock')[:8]
            )

            # ── Clientes activos vs inactivos ────────────────────────────
            clientes_activos   = Cliente.objects.filter(estado='activo').count()
            clientes_inactivos = Cliente.objects.filter(estado='inactivo').count()

        except Exception:
            total_productos = total_clientes = total_ventas = 0
            total_proveedores = total_compras = total_reportes = 0
            ingresos = 0
            meses_labels = meses_data = ingresos_data = compras_data = []
            top_productos_labels = top_productos_data = []
            stock_bajo = []
            clientes_activos = clientes_inactivos = 0

        return render(request, 'Inicio/index.html', {
            # Totales
            'total_productos':   total_productos,
            'total_clientes':    total_clientes,
            'total_ventas':      total_ventas,
            'total_proveedores': total_proveedores,
            'total_compras':     total_compras,
            'total_reportes':    total_reportes,
            'ingresos_totales':  ingresos,
            # Gráficas (JSON para JS)
            'meses_labels':           json.dumps(meses_labels),
            'ventas_por_mes':         json.dumps(meses_data),
            'ingresos_por_mes':       json.dumps(ingresos_data),
            'compras_por_mes':        json.dumps(compras_data),
            'top_productos_labels':   json.dumps(top_productos_labels),
            'top_productos_data':     json.dumps(top_productos_data),
            'clientes_activos':       clientes_activos,
            'clientes_inactivos':     clientes_inactivos,
            # Stock bajo
            'stock_bajo':        stock_bajo,
            'stock_bajo_count':  len(list(stock_bajo)),
        })


index = IndexView.as_view()


@admin_login_required
def notificaciones_data(request):
    data = notificaciones(request)
    lista = data.get('notificaciones', [])[:20]
    payload = []
    for n in lista:
        payload.append({
            'tipo':     n.get('tipo', 'info'),
            'icono':    n.get('icono', '🔔'),
            'mensaje':  n.get('mensaje', ''),
            'url':      n.get('url', '#'),
            'prioridad':n.get('prioridad', 4),
            'notif_id': n.get('notif_id', None),
        })
    return JsonResponse({
        'ok': True,
        'total_notificaciones': data.get('total_notificaciones', 0),
        'notificaciones': payload,
    })


@login_required
def limpiar_notificaciones(request):
    from app.models import NotificacionEmail
    if request.method == 'POST':
        total = NotificacionEmail.objects.filter(usuario=request.user).delete()[0]
        return JsonResponse({'ok': True, 'eliminadas': total})
    return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)


@login_required
def marcar_leida_notificacion(request, id):
    from django.shortcuts import get_object_or_404
    from app.models import NotificacionEmail
    if request.method == 'POST':
        notif = get_object_or_404(NotificacionEmail, id=id, usuario=request.user)
        notif.leida = True
        notif.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)


@login_required
def eliminar_notificacion(request, id):
    from django.shortcuts import get_object_or_404
    from app.models import NotificacionEmail
    if request.method == 'POST':
        notif = get_object_or_404(NotificacionEmail, id=id, usuario=request.user)
        notif.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)
