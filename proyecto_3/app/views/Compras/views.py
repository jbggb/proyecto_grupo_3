"""Vistas para gestión de compras"""
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from app.decorators import admin_login_required
from ...models import Compra, Proveedor, Producto, Administrador


def _validar_fecha_nueva(fecha_str):
    try:
        fecha = date.fromisoformat(fecha_str)
    except ValueError:
        return None, 'La fecha no tiene un formato válido.'
    hoy = date.today()
    limite = hoy + timedelta(days=7)
    if fecha < hoy:
        return None, f'La fecha no puede ser anterior a hoy ({hoy.strftime("%d/%m/%Y")}).'
    if fecha > limite:
        return None, f'La fecha no puede ser mayor a 7 días desde hoy ({limite.strftime("%d/%m/%Y")}).'
    return fecha, None


def _validar_fecha_editar(fecha_str):
    try:
        return date.fromisoformat(fecha_str), None
    except ValueError:
        return None, 'La fecha no tiene un formato válido.'


def _get_admin_de_sesion(request):
    """Obtiene el administrador actualmente logueado desde la sesión."""
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return None
    try:
        return Administrador.objects.get(id=admin_id)
    except Administrador.DoesNotExist:
        return None


@method_decorator(admin_login_required, name='dispatch')
class ComprasView(View):
    def get(self, request):
        hoy = date.today()
        lista_compras = Compra.objects.select_related('Administrador', 'Producto', 'Proveedor').all().order_by('-fechaCompra')

        busqueda = request.GET.get('busqueda', '').strip()
        if busqueda:
            lista_compras = (
                lista_compras.filter(Proveedor__nombre__icontains=busqueda) |
                lista_compras.filter(Producto__nombre__icontains=busqueda)
            )

        estado_filtro = request.GET.get('estado', '').strip()
        if estado_filtro == 'Completada':
            lista_compras = lista_compras.filter(estado='Completada')
        elif estado_filtro == 'Pendiente':
            lista_compras = lista_compras.filter(estado='Pendiente')

        return render(request, 'Compras/Compras.html', {
            'compras':          lista_compras,
            'proveedores':      Proveedor.objects.all(),
            'productos':        Producto.objects.all(),
            'administradores':  Administrador.objects.all(),
            'fecha_min':        hoy.strftime('%Y-%m-%d'),
            'fecha_max':        (hoy + timedelta(days=7)).strftime('%Y-%m-%d'),
        })


@method_decorator(admin_login_required, name='dispatch')
class CrearCompraView(View):
    def post(self, request):
        try:
            fecha_str    = request.POST.get('fecha', '').strip()
            estado_str   = request.POST.get('estado', 'Pendiente').strip()
            producto_id  = request.POST.get('producto_id', '').strip()
            proveedor_id = request.POST.get('proveedor_id', '').strip()

            if not fecha_str or not producto_id or not proveedor_id:
                messages.error(request, 'Fecha, producto y proveedor son obligatorios.')
                return redirect('compras')

            fecha, error = _validar_fecha_nueva(fecha_str)
            if error:
                messages.error(request, error)
                return redirect('compras')

            admin = _get_or_create_admin()
            if not admin:
                messages.error(request, 'No hay administradores registrados.')
                return redirect('compras')

            Compra.objects.create(
                fechaCompra=fecha,
                estado=estado_str,
                Administrador=admin,
                Producto_id=int(producto_id),
                Proveedor_id=int(proveedor_id),
            )
            messages.success(request, 'Compra registrada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear la compra: {str(e)}')
        return redirect('compras')


@method_decorator(admin_login_required, name='dispatch')
class EditarCompraView(View):
    def post(self, request, id):
        compra = get_object_or_404(Compra, idCompra=id)
        try:
            fecha_str    = request.POST.get('fecha', '').strip()
            estado_str   = request.POST.get('estado', 'Pendiente').strip()
            producto_id  = request.POST.get('producto_id', '').strip()
            proveedor_id = request.POST.get('proveedor_id', '').strip()

            if not fecha_str or not producto_id or not proveedor_id:
                messages.error(request, 'Fecha, producto y proveedor son obligatorios.')
                return redirect('compras')

            fecha, error = _validar_fecha_editar(fecha_str)
            if error:
                messages.error(request, error)
                return redirect('compras')

            admin = _get_or_create_admin()
            if not admin:
                messages.error(request, 'No hay administradores registrados.')
                return redirect('compras')

            compra.fechaCompra   = fecha
            compra.estado        = estado_str
            compra.Administrador = admin
            compra.Producto_id   = int(producto_id)
            compra.Proveedor_id  = int(proveedor_id)
            compra.save()
            messages.success(request, 'Compra actualizada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
        return redirect('compras')

@method_decorator(admin_login_required, name='dispatch')
class EliminarCompraView(View):
    def post(self, request, id):
        compra = get_object_or_404(Compra, idCompra=id)
        try:
            compra.delete()
            messages.success(request, 'Compra eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
        return redirect('compras')


@method_decorator(admin_login_required, name='dispatch')
class ComprasJsonView(View):
    def get(self, request):
        lista = [
            {
                'id':             c.idCompra,
                'fecha':          str(c.fechaCompra),
                'estado':         c.estado,
                'administrador':  c.Administrador.nombre if c.Administrador else '',
                'producto':       c.Producto.nombre      if c.Producto      else '',
                'proveedor':      c.Proveedor.nombre     if c.Proveedor     else '',
            }
            for c in Compra.objects.select_related('Administrador', 'Producto', 'Proveedor').order_by('-fechaCompra')
        ]
        return JsonResponse({'compras': lista})


compras               = ComprasView.as_view()
crear_compra          = CrearCompraView.as_view()
modal_editar_compra   = EditarCompraView.as_view()
modal_eliminar_compra = EliminarCompraView.as_view()
compras_json          = ComprasJsonView.as_view()