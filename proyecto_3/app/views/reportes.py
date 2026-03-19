from django.shortcuts import render
from django.views.generic import View
from django.views import View as DjangoView
from django.http import HttpResponse
from app.models import Proveedor, Producto, Cliente, Venta, Compra
from app.utils import exportar_pdf, exportar_excel
from datetime import datetime

# ====== VISTAS PARA EXPORTAR REPORTES ======
class ExportarProveedoresPDF(DjangoView):
    def get(self, request):
        
        proveedores = Proveedor.objects.all()  # ← corregido
        
        columnas = ['ID', 'Nombre', 'Teléfono', 'Email', 'Envío']
        
        datos = [
            (p.id, p.nombre, p.telefono, p.email, p.envio)
            for p in proveedores  # ← corregido
        ]
        nombre_archivo = f'Reporte_Proveedores_{datetime.now().strftime("%d_%m_%Y")}'
        
        return exportar_pdf(
            titulo='REPORTE DE PROVEEDORES',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo,
        )

class ExportarProveedoresExcel(DjangoView):
    def get(self, request):
        
        proveedores = Proveedor.objects.all()  # ← corregido
        
        columnas = ['ID', 'Nombre', 'Teléfono', 'Email', 'Envío']
        
        datos = [
            (p.id, p.nombre, p.telefono, p.email, p.envio)
            for p in proveedores  # ← corregido
        ]
        
        nombre_archivo = f'Reporte_Proveedores_{datetime.now().strftime("%d_%m_%Y")}'
        
        return exportar_excel(
            titulo='REPORTE DE PROVEEDORES',
            columnas=columnas,
            datos=datos,
            nombre_archivo=nombre_archivo
        )
        
# ====== PRODUCTOS ======
class ExportarProductosPDF(DjangoView):
    def get(self, request):
        productos = Producto.objects.all()
        columnas = ['ID', 'Nombre', 'Precio', 'Stock']
        datos = [(p.idProducto, p.nombre, p.precio, p.stock) for p in productos]
        return exportar_pdf(
            titulo='REPORTE DE PRODUCTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=f'Reporte_Productos_{datetime.now().strftime("%d_%m_%Y")}',
        )

class ExportarProductosExcel(DjangoView):
    def get(self, request):
        productos = Producto.objects.all()
        columnas = ['ID', 'Nombre', 'Precio', 'Stock']
        datos = [(p.idProducto, p.nombre, p.precio, p.stock) for p in productos]
        return exportar_excel(
            titulo='REPORTE DE PRODUCTOS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=f'Reporte_Productos_{datetime.now().strftime("%d_%m_%Y")}',
        )

# ====== CLIENTES ======
class ExportarClientesPDF(DjangoView):
    def get(self, request):
        clientes = Cliente.objects.all()
        columnas = ['ID', 'Nombre', 'Documento', 'Teléfono', 'Email', 'Estado']
        datos = [(c.id, c.nombre, c.documento, c.telefono, c.email, c.estado) for c in clientes]
        return exportar_pdf(
            titulo='REPORTE DE CLIENTES',
            columnas=columnas,
            datos=datos,
            nombre_archivo=f'Reporte_Clientes_{datetime.now().strftime("%d_%m_%Y")}',
        )

class ExportarClientesExcel(DjangoView):
    def get(self, request):
        clientes = Cliente.objects.all()
        columnas = ['ID', 'Nombre', 'Documento', 'Teléfono', 'Email', 'Estado']
        datos = [(c.id, c.nombre, c.documento, c.telefono, c.email, c.estado) for c in clientes]
        return exportar_excel(
            titulo='REPORTE DE CLIENTES',
            columnas=columnas,
            datos=datos,
            nombre_archivo=f'Reporte_Clientes_{datetime.now().strftime("%d_%m_%Y")}',
        )

# ====== VENTAS ======
class ExportarVentasPDF(DjangoView):
    def get(self, request):
        ventas = Venta.objects.all()
        columnas = ['ID', 'Cliente', 'Fecha', 'Total', 'Estado']
        datos = [(v.id, v.cliente, v.fecha.replace(tzinfo=None), v.total, v.estado) for v in ventas]
        return exportar_pdf(
            titulo='REPORTE DE VENTAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=f'Reporte_Ventas_{datetime.now().strftime("%d_%m_%Y")}',
        )

class ExportarVentasExcel(DjangoView):
    def get(self, request):
        ventas = Venta.objects.all()
        columnas = ['ID', 'Cliente', 'Fecha', 'Total', 'Estado']
        datos = [(v.id, v.cliente, v.fecha.replace(tzinfo=None), v.total, v.estado) for v in ventas]
        return exportar_excel(
            titulo='REPORTE DE VENTAS',
            columnas=columnas,
            datos=datos,
            nombre_archivo=f'Reporte_Ventas_{datetime.now().strftime("%d_%m_%Y")}',
        )

# ====== COMPRAS ======
class ExportarComprasPDF(DjangoView):
    def get(self, request):
        compras = Compra.objects.select_related('Producto', 'Proveedor').all()
        columnas = ['ID', 'Fecha', 'Producto', 'Proveedor', 'Estado']
        datos = [(c.idCompra, c.fechaCompra, c.Producto.nombre if c.Producto else '-', c.Proveedor.nombre if c.Proveedor else '-', c.estado) for c in compras]
        return exportar_pdf(titulo='REPORTE DE COMPRAS', columnas=columnas, datos=datos,
            nombre_archivo=f'Reporte_Compras_{datetime.now().strftime("%d_%m_%Y")}')

class ExportarComprasExcel(DjangoView):
    def get(self, request):
        compras = Compra.objects.select_related('Producto', 'Proveedor').all()
        columnas = ['ID', 'Fecha', 'Producto', 'Proveedor', 'Estado']
        datos = [(c.idCompra, c.fechaCompra, c.Producto.nombre if c.Producto else '-', c.Proveedor.nombre if c.Proveedor else '-', c.estado) for c in compras]
        return exportar_excel(titulo='REPORTE DE COMPRAS', columnas=columnas, datos=datos,
            nombre_archivo=f'Reporte_Compras_{datetime.now().strftime("%d_%m_%Y")}')
        