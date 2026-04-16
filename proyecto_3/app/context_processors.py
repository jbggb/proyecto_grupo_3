# app/context_processors.py
"""
Context processor mejorado con múltiples tipos de notificaciones.
Inyecta notificaciones automáticamente en TODOS los templates.
"""

from datetime import date, timedelta
from datetime import datetime
from django.db.models import Sum, Count
from django.utils import timezone
from app.models import Producto, Compra, Venta, DetalleVenta, NotificacionEmail
from django.contrib.auth.models import User

# Umbrales configurables
UMBRAL_STOCK_BAJO = 5    # unidades
DIAS_COMPRA_VENCER = 3   # días
META_VENTAS_MENSUAL = 5000000  # 5 millones de pesos


def notificaciones(request):
    """
    Retorna todas las notificaciones del sistema.
    Se pasa automáticamente a todos los templates.
    """
    # Solo calcular si el usuario está autenticado
    if not request.user.is_authenticated:
        return {
            'notificaciones': [],
            'total_notificaciones': 0,
            'notif_stock_bajo': [],
            'notif_compras_vencer': [],
            'notif_total': 0,
        }

    notificaciones_lista = []
    hoy = date.today()

    try:
        # =========================================================
        # NOTIFICACIONES DEL USUARIO (de la BD)
        # =========================================================
        notif_usuario = NotificacionEmail.objects.filter(
            usuario=request.user,
            leida=False
        ).order_by('-fecha_creacion')[:10]

        for notif in notif_usuario:
            # Determinar URL según el tipo de notificación
            url = '#'
            if 'compra' in notif.asunto.lower():
                url = '/compras/'
            elif 'venta' in notif.asunto.lower():
                url = '/ventas/'
            elif 'stock' in notif.asunto.lower() or 'agotado' in notif.asunto.lower():
                url = '/productos/'
            elif 'proveedor' in notif.asunto.lower():
                url = '/proveedores/'

            notificaciones_lista.append({
                'tipo': notif.tipo,
                'icono': {
                    'alerta': '⚠️',
                    'info': 'ℹ️',
                    'error': '❌',
                    'success': '✅',
                }.get(notif.tipo, '🔔'),
                'mensaje': notif.asunto,
                'url': url,
                'fecha': notif.fecha_creacion,
                'prioridad': 1 if notif.tipo == 'error' else 2 if notif.tipo == 'alerta' else 3,
                'notif_id': notif.id,
            })

        # =========================================================
        # 1. PRODUCTOS CON STOCK BAJO (CRÍTICO)
        # =========================================================
        stock_bajo = Producto.objects.filter(stock__lte=UMBRAL_STOCK_BAJO).order_by('stock')
        for prod in stock_bajo:
            if prod.stock == 0:
                nivel = 'error'
                icono = '❌'
                mensaje = f'AGOTADO: {prod.nombre} - Sin unidades disponibles'
            elif prod.stock <= 2:
                nivel = 'error'
                icono = '🔴'
                mensaje = f'Stock CRÍTICO: {prod.nombre} (solo {prod.stock} unidades)'
            else:
                nivel = 'warning'
                icono = '⚠️'
                mensaje = f'Stock bajo: {prod.nombre} ({prod.stock} unidades restantes)'

            notificaciones_lista.append({
                'tipo': nivel,
                'icono': icono,
                'mensaje': mensaje,
                'url': '/productos/',
                'fecha': timezone.now(),
                'prioridad': 1 if prod.stock == 0 else 2
            })

        # =========================================================
        # 2. COMPRAS PENDIENTES PRÓXIMAS A VENCER
        # =========================================================
        limite = hoy + timedelta(days=DIAS_COMPRA_VENCER)
        compras_vencer = Compra.objects.filter(
            estado='Pendiente',
            fechaCompra__lte=limite
        ).select_related('Producto', 'Proveedor').order_by('fechaCompra')

        for compra in compras_vencer:
            dias_restantes = (compra.fechaCompra - hoy).days
            producto_nombre = compra.Producto.nombre if compra.Producto else 'Producto sin asignar'
            if dias_restantes == 0:
                nivel = 'error'
                icono = '🚨'
                mensaje = f'Compra #{compra.idCompra} - {producto_nombre} VENCE HOY'
            elif dias_restantes == 1:
                nivel = 'warning'
                icono = '⚠️'
                mensaje = f'Compra #{compra.idCompra} - {producto_nombre} vence MAÑANA'
            else:
                nivel = 'info'
                icono = '📅'
                mensaje = f'Compra #{compra.idCompra} - {producto_nombre} vence en {dias_restantes} días'

            notificaciones_lista.append({
                'tipo': nivel,
                'icono': icono,
                'mensaje': mensaje,
                'url': '/compras/',
                'fecha': compra.fechaCompra,
                'prioridad': 1 if dias_restantes <= 1 else 2
            })

        # =========================================================
        # 3. PRODUCTOS AGOTADOS (RESUMEN)
        # =========================================================
        agotados = Producto.objects.filter(stock=0).count()
        if agotados > 0:
            notificaciones_lista.append({
                'tipo': 'error',
                'icono': '❌',
                'mensaje': f'{agotados} producto(s) están AGOTADOS - ¡Reabastecer urgentemente!',
                'url': '/productos/?stock=0',
                'fecha': timezone.now(),
                'prioridad': 1
            })

        # =========================================================
        # 4. VENTAS DEL DÍA
        # =========================================================
        ventas_hoy = Venta.objects.filter(fecha__date=hoy).count()
        if ventas_hoy > 0:
            total_hoy = Venta.objects.filter(fecha__date=hoy).aggregate(
                total=Sum('total')
            )['total'] or 0

            nivel = 'success' if ventas_hoy > 5 else 'info'
            notificaciones_lista.append({
                'tipo': nivel,
                'icono': '💰',
                'mensaje': f'{ventas_hoy} venta(s) hoy - Total: ${total_hoy:,.0f} COP',
                'url': '/ventas/',
                'fecha': timezone.now(),
                'prioridad': 3
            })

        # =========================================================
        # 5. TOP PRODUCTOS MÁS VENDIDOS (ESTADÍSTICAS)
        # =========================================================
        top_productos = DetalleVenta.objects.values('producto_nombre').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido')[:3]

        if top_productos:
            mensaje_top = "🏆 Más vendidos: "
            for i, prod in enumerate(top_productos):
                if i > 0:
                    mensaje_top += " | "
                mensaje_top += f"{prod['producto_nombre']} ({prod['total_vendido']} uds)"

            notificaciones_lista.append({
                'tipo': 'info',
                'icono': '🏆',
                'mensaje': mensaje_top,
                'url': '/reportes/',
                'fecha': timezone.now(),
                'prioridad': 4
            })

        # =========================================================
        # 6. NUEVOS USUARIOS (ÚLTIMOS 7 DÍAS)
        # =========================================================
        hace_7_dias = hoy - timedelta(days=7)
        nuevos_usuarios = User.objects.filter(date_joined__date__gte=hace_7_dias).count()

        if nuevos_usuarios > 0:
            notificaciones_lista.append({
                'tipo': 'info',
                'icono': '👤',
                'mensaje': f'{nuevos_usuarios} usuario(s) nuevo(s) en los últimos 7 días',
                'url': '/usuarios/listar/',
                'fecha': timezone.now(),
                'prioridad': 4
            })

        # =========================================================
        # 7. META DE VENTAS DEL MES
        # =========================================================
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        ventas_mes = Venta.objects.filter(
            fecha__month=mes_actual,
            fecha__year=anio_actual
        ).aggregate(total=Sum('total'))['total'] or 0

        if ventas_mes > 0:
            porcentaje = (ventas_mes / META_VENTAS_MENSUAL) * 100
            if porcentaje >= 100:
                nivel = 'success'
                icono = '🎉'
                mensaje = f'¡META DEL MES ALCANZADA! Total: ${ventas_mes:,.0f} COP'
            elif porcentaje >= 75:
                nivel = 'success'
                icono = '📈'
                restante = META_VENTAS_MENSUAL - ventas_mes
                mensaje = f'Meta mensual: {porcentaje:.0f}% - Faltan ${restante:,.0f} COP'
            elif porcentaje >= 50:
                nivel = 'info'
                icono = '📊'
                restante = META_VENTAS_MENSUAL - ventas_mes
                mensaje = f'Meta mensual: {porcentaje:.0f}% - Faltan ${restante:,.0f} COP'
            else:
                nivel = 'warning'
                icono = '🎯'
                restante = META_VENTAS_MENSUAL - ventas_mes
                mensaje = f'Meta mensual: {porcentaje:.0f}% - Faltan ${restante:,.0f} COP'

            notificaciones_lista.append({
                'tipo': nivel,
                'icono': icono,
                'mensaje': mensaje,
                'url': '/reportes/',
                'fecha': timezone.now(),
                'prioridad': 3
            })

        # =========================================================
        # 8. USUARIOS INACTIVOS (30+ DÍAS SIN LOGIN)
        # =========================================================
        limite_inactivo = timezone.now() - timedelta(days=30)
        usuarios_inactivos = User.objects.filter(last_login__lt=limite_inactivo).count()

        if usuarios_inactivos > 3:  # Solo notificar si hay más de 3
            notificaciones_lista.append({
                'tipo': 'warning',
                'icono': '😴',
                'mensaje': f'{usuarios_inactivos} usuario(s) inactivos por más de 30 días',
                'url': '/usuarios/listar/',
                'fecha': timezone.now(),
                'prioridad': 3
            })

        # =========================================================
        # 9. PROVEEDORES CON ENTREGAS PENDIENTES ATRASADAS
        # =========================================================
        compras_atrasadas = Compra.objects.filter(
            estado='Pendiente',
            fechaCompra__lt=hoy
        ).values('Proveedor__nombre').annotate(total=Count('idCompra'))

        for proveedor in compras_atrasadas:
            notificaciones_lista.append({
                'tipo': 'error',
                'icono': '🚛',
                'mensaje': f'Proveedor "{proveedor["Proveedor__nombre"]}" tiene {proveedor["total"]} compra(s) atrasada(s)',
                'url': '/compras/',
                'fecha': timezone.now(),
                'prioridad': 1
            })

        # =========================================================
        # 10. PRODUCTOS CON EXCESO DE STOCK
        # =========================================================
        exceso_stock = Producto.objects.filter(stock__gte=100).count()
        if exceso_stock > 0:
            notificaciones_lista.append({
                'tipo': 'info',
                'icono': '📦',
                'mensaje': f'{exceso_stock} producto(s) con exceso de stock (+100 unidades)',
                'url': '/productos/',
                'fecha': timezone.now(),
                'prioridad': 4
            })

        # =========================================================
        # ORDENAR NOTIFICACIONES POR PRIORIDAD (1 = más importante)
        # =========================================================
        notificaciones_lista.sort(key=lambda x: x['prioridad'])

    except Exception as e:
        # Si hay error, devolver lista vacía (no romper el sitio)
        print(f"Error en notificaciones: {e}")
        notificaciones_lista = []

    # Datos para compatibilidad con tu código existente
    stock_bajo_list = list(Producto.objects.filter(stock__lte=UMBRAL_STOCK_BAJO).values('idProducto', 'nombre', 'stock')[:10])
    compras_vencer_list = list(Compra.objects.filter(
        estado='Pendiente',
        fechaCompra__lte=hoy + timedelta(days=DIAS_COMPRA_VENCER)
    ).values('idCompra', 'fechaCompra', 'Producto__nombre', 'Proveedor__nombre')[:10])

    return {
        'notificaciones': notificaciones_lista,           # Nueva lista completa
        'total_notificaciones': len(notificaciones_lista), # Total de notificaciones
        'notif_stock_bajo': stock_bajo_list,              # Compatibilidad con código anterior
        'notif_compras_vencer': compras_vencer_list,      # Compatibilidad con código anterior
        'notif_total': len(stock_bajo_list) + len(compras_vencer_list),  # Compatibilidad
    }
