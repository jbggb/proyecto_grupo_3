"""Vista principal del sistema"""
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from app.decorators import admin_login_required
from ...models import Producto, Cliente, Venta, Proveedor, Compra, Reporte


@method_decorator(admin_login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        try:
            total_productos  = Producto.objects.count()
            total_clientes   = Cliente.objects.count()
            total_ventas     = Venta.objects.count()
            total_proveedores = Proveedor.objects.count()
            total_compras    = Compra.objects.count()
            total_reportes   = Reporte.objects.count()
        except:
            total_productos = total_clientes = total_ventas = 0
            total_proveedores = total_compras = total_reportes = 0

        return render(request, 'Inicio/index.html', {
            'total_productos':  total_productos,
            'total_clientes':   total_clientes,
            'total_ventas':     total_ventas,
            'total_proveedores': total_proveedores,
            'total_compras':    total_compras,
            'total_reportes':   total_reportes,
        })


index = IndexView.as_view()