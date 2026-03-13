"""Vistas para gestión de productos"""
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from app.decorators import admin_login_required
from app.models import Producto, Marca, TipoProductos, unidad_medida


def _contexto_productos(query='', form_data=None):
    """Construye el contexto base. form_data preserva valores del modal si hay error."""
    lista = Producto.objects.all()
    if query:
        lista = lista.filter(nombre__icontains=query)
    return {
        'productos': lista,
        'marcas':    Marca.objects.all(),
        'tipos':     TipoProductos.objects.all(),
        'unidades':  unidad_medida.objects.all(),
        'form_data': form_data or {},   # ← datos a re-inyectar en el modal
    }


@method_decorator(admin_login_required, name='dispatch')
class ProductosView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        return render(request, 'Productos/productos.html', _contexto_productos(query))


@method_decorator(admin_login_required, name='dispatch')
class CrearProductoView(View):
    def post(self, request):
        # Capturar datos del POST para poder re-mostrarlos si hay error
        form_data = {
            'nombre':   request.POST.get('nombre', '').strip(),
            'precio':   request.POST.get('precio', '').strip(),
            'stock':    request.POST.get('stock', '').strip(),
            'idMarca':  request.POST.get('idMarca', ''),
            'idTipo':   request.POST.get('idTipo', ''),
            'idUnidad': request.POST.get('idUnidad', ''),
        }

        def error(msg):
            messages.error(request, msg)
            ctx = _contexto_productos(form_data=form_data)
            ctx['abrir_modal_agregar'] = True   # señal para el template
            return render(request, 'Productos/productos.html', ctx)

        nombre   = form_data['nombre']
        precio   = form_data['precio']
        stock    = form_data['stock']
        idMarca  = form_data['idMarca']
        idTipo   = form_data['idTipo']
        idUnidad = form_data['idUnidad']

        if not nombre:
            return error('El nombre es obligatorio.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
            return error('El nombre solo puede contener letras y espacios.')
        if Marca.objects.filter(nombreMarca__iexact=nombre).exists():
            return error(f'"{nombre}" ya existe como Marca.')
        if TipoProductos.objects.filter(nombre_tipo__iexact=nombre).exists():
            return error(f'"{nombre}" ya existe como Tipo de producto.')
        if unidad_medida.objects.filter(nombre_unidad__iexact=nombre).exists():
            return error(f'"{nombre}" ya existe como Unidad de medida.')
        if Producto.objects.filter(nombre__iexact=nombre, idMarca=idMarca, idTipo=idTipo).exists():
            return error(f'Ya existe un producto "{nombre}" con esa marca y tipo.')
        if not precio.isdigit() or int(precio) < 1 or int(precio) > 800000:
            return error('El precio debe ser un número entre 1 y 800.000.')
        if not stock.isdigit() or int(stock) < 0 or int(stock) > 1000:
            return error('El stock debe ser un número entre 0 y 1.000.')

        try:
            Producto.objects.create(
                nombre=nombre, precio=precio, stock=stock,
                idMarca=get_object_or_404(Marca, idMarca=idMarca),
                idTipo=get_object_or_404(TipoProductos, idTipo=idTipo),
                idUnidad=get_object_or_404(unidad_medida, idUnidad=idUnidad),
            )
            messages.success(request, f'Producto "{nombre}" creado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el producto: {str(e)}')

        return redirect('productos')


@method_decorator(admin_login_required, name='dispatch')
class EditarProductoView(View):
    def post(self, request, id):
        producto = get_object_or_404(Producto, idProducto=id)
        nombre   = request.POST.get('nombre', '').strip()
        precio   = request.POST.get('precio', '').strip()
        stock    = request.POST.get('stock', '').strip()
        idMarca  = request.POST.get('idMarca')
        idTipo   = request.POST.get('idTipo')
        idUnidad = request.POST.get('idUnidad')

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.'); return redirect('productos')
        if Marca.objects.filter(nombreMarca__iexact=nombre).exists():
            messages.error(request, f'"{nombre}" ya existe como Marca.'); return redirect('productos')
        if TipoProductos.objects.filter(nombre_tipo__iexact=nombre).exists():
            messages.error(request, f'"{nombre}" ya existe como Tipo de producto.'); return redirect('productos')
        if unidad_medida.objects.filter(nombre_unidad__iexact=nombre).exists():
            messages.error(request, f'"{nombre}" ya existe como Unidad de medida.'); return redirect('productos')
        if Producto.objects.filter(nombre__iexact=nombre, idMarca=idMarca, idTipo=idTipo).exclude(idProducto=id).exists():
            messages.error(request, f'Ya existe un producto "{nombre}" con esa marca y tipo.'); return redirect('productos')
        if not precio.isdigit() or int(precio) < 1 or int(precio) > 800000:
            messages.error(request, 'El precio debe ser un número entre 1 y 800.000.'); return redirect('productos')
        if not stock.isdigit() or int(stock) < 0 or int(stock) > 1000:
            messages.error(request, 'El stock debe ser un número entre 0 y 1.000.'); return redirect('productos')

        producto.nombre   = nombre
        producto.precio   = precio
        producto.stock    = stock
        producto.idMarca  = get_object_or_404(Marca, idMarca=idMarca)
        producto.idTipo   = get_object_or_404(TipoProductos, idTipo=idTipo)
        producto.idUnidad = get_object_or_404(unidad_medida, idUnidad=idUnidad)
        producto.save()
        messages.success(request, f'Producto "{nombre}" actualizado correctamente.')
        return redirect('productos')


@method_decorator(admin_login_required, name='dispatch')
class EliminarProductoView(View):
    def post(self, request, id):
        try:
            producto = get_object_or_404(Producto, idProducto=id)
            nombre   = producto.nombre
            producto.delete()
            messages.success(request, f'Producto "{nombre}" eliminado correctamente.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        return redirect('productos')


productos         = ProductosView.as_view()
crear_producto    = CrearProductoView.as_view()
editar_producto   = EditarProductoView.as_view()
eliminar_producto = EliminarProductoView.as_view()