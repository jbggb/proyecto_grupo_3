"""Vistas para gestión de productos"""
import re
import json
import urllib.request
import urllib.error
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from app.decorators import admin_login_required
from app.models import Producto, Marca, TipoProductos, unidad_medida
from app.services.notifications import notificacion_stock_bajo


def _contexto_productos(query='', stock_filter='', form_data=None):
    """Construye el contexto base. form_data preserva valores del modal si hay error."""
    lista = Producto.objects.all()
    if query:
        lista = lista.filter(nombre__icontains=query)
    if stock_filter == 'disponible':
        lista = lista.filter(stock__gt=5)
    elif stock_filter == 'bajo':
        lista = lista.filter(stock__gt=0, stock__lte=5)
    elif stock_filter == 'agotado':
        lista = lista.filter(stock=0)
    return {
        'productos': lista,
        'marcas':    Marca.objects.all(),
        'tipos':     TipoProductos.objects.all(),
        'unidades':  unidad_medida.objects.all(),
        'form_data': form_data or {},
    }


@method_decorator(admin_login_required, name='dispatch')
class ProductosView(View):
    def get(self, request):
        query        = request.GET.get('q', '')
        stock_filter = request.GET.get('stock', '')
        return render(request, 'Productos/productos.html', _contexto_productos(query, stock_filter))


@method_decorator(admin_login_required, name='dispatch')
class CrearProductoView(View):
    def post(self, request):
        form_data = {
            'nombre':        request.POST.get('nombre', '').strip(),
            'precio':        request.POST.get('precio', '').strip(),
            'stock':         request.POST.get('stock', '').strip(),
            'idMarca':       request.POST.get('idMarca', ''),
            'idTipo':        request.POST.get('idTipo', ''),
            'idUnidad':      request.POST.get('idUnidad', ''),
            'codigo_barras': request.POST.get('codigo_barras', '').strip(),
        }

        def error(msg):
            messages.error(request, msg)
            ctx = _contexto_productos(form_data=form_data)
            ctx['abrir_modal_agregar'] = True
            return render(request, 'Productos/productos.html', ctx)

        nombre   = form_data['nombre']
        precio   = form_data['precio']
        stock    = form_data['stock']
        idMarca  = form_data['idMarca']
        idTipo   = form_data['idTipo']
        idUnidad = form_data['idUnidad']
        codigo_barras = form_data['codigo_barras']

        if not nombre:
            return error('El nombre es obligatorio.')
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚüÜñÑ\s\-\.%&/]+$', nombre):
            return error('El nombre solo puede contener letras y espacios.')
        if Marca.objects.filter(nombreMarca__iexact=nombre).exists():
            return error(f'"{nombre}" ya existe como Marca.')
        if TipoProductos.objects.filter(nombre_tipo__iexact=nombre).exists():
            return error(f'"{nombre}" ya existe como Tipo de producto.')
        if unidad_medida.objects.filter(nombre_unidad__iexact=nombre).exists():
            return error(f'"{nombre}" ya existe como Unidad de medida.')
        if Producto.objects.filter(nombre__iexact=nombre, idMarca=idMarca, idTipo=idTipo).exists():
            return error(f'Ya existe un producto "{nombre}" con esa marca y tipo.')

        try:
            precio_val = float(precio.replace(',', '.'))
            if precio_val < 1 or precio_val > 800000:
                raise ValueError
        except ValueError:
            return error('El precio debe ser un número entre 1 y 800.000.')

        if not stock.isdigit() or int(stock) < 0 or int(stock) > 1000:
            return error('El stock debe ser un número entre 0 y 1.000.')

        try:
            producto = Producto.objects.create(
                nombre=nombre,
                precio=precio_val,
                stock=int(stock),
                idMarca=get_object_or_404(Marca, idMarca=idMarca),
                idTipo=get_object_or_404(TipoProductos, idTipo=idTipo),
                idUnidad=get_object_or_404(unidad_medida, idUnidad=idUnidad),
                codigo_barras=codigo_barras,
            )
            if producto.stock <= 5:
                notificacion_stock_bajo(producto)
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

        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return redirect('productos')
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚüÜñÑ\s\-\.%&/]+$', nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.')
            return redirect('productos')
        if Marca.objects.filter(nombreMarca__iexact=nombre).exists():
            messages.error(request, f'"{nombre}" ya existe como Marca.')
            return redirect('productos')
        if TipoProductos.objects.filter(nombre_tipo__iexact=nombre).exists():
            messages.error(request, f'"{nombre}" ya existe como Tipo de producto.')
            return redirect('productos')
        if unidad_medida.objects.filter(nombre_unidad__iexact=nombre).exists():
            messages.error(request, f'"{nombre}" ya existe como Unidad de medida.')
            return redirect('productos')
        if Producto.objects.filter(nombre__iexact=nombre, idMarca=idMarca, idTipo=idTipo).exclude(idProducto=id).exists():
            messages.error(request, f'Ya existe un producto "{nombre}" con esa marca y tipo.')
            return redirect('productos')

        try:
            precio_val = float(precio.replace(',', '.'))
        except ValueError:
            messages.error(request, 'El precio debe ser un número válido.')
            return redirect('productos')
        if precio_val < 1 or precio_val > 800000:
            messages.error(request, 'El precio debe ser un número entre 1 y 800.000.')
            return redirect('productos')
        if not stock.isdigit() or int(stock) < 0 or int(stock) > 1000:
            messages.error(request, 'El stock debe ser un número entre 0 y 1.000.')
            return redirect('productos')

        producto.nombre   = nombre
        producto.precio   = precio_val
        producto.stock    = int(stock)
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


# ──────────────────────────────────────────────────────────────────
#  ESCÁNER DE CÓDIGO DE BARRAS
# ──────────────────────────────────────────────────────────────────

@method_decorator(admin_login_required, name='dispatch')
class BuscarCodigoBarrasView(View):
    """
    Endpoint AJAX: busca el producto por codigo_barras en la BD.
    Si no existe, consulta Open Food Facts para sugerir el nombre.
    """
    def get(self, request):
        codigo = request.GET.get('codigo', '').strip()
        if not codigo:
            return JsonResponse({'status': 'error', 'mensaje': 'Código vacío.'})

        # 1. Buscar en BD local por campo codigo_barras exacto
        producto = Producto.objects.filter(codigo_barras=codigo).first()
        if producto:
            return JsonResponse({
                'status':       'encontrado',
                'id':           producto.idProducto,
                'nombre':       producto.nombre,
                'stock_actual': producto.stock,
                'precio':       str(producto.precio),
                'marca':        producto.idMarca.nombreMarca,
            })

        # 2. No está en BD → consultar Open Food Facts para sugerir nombre
        nombre_sugerido = _consultar_open_food_facts(codigo)

        return JsonResponse({
            'status':          'nuevo',
            'nombre_sugerido': nombre_sugerido or '',
            'codigo':          codigo,
        })


@method_decorator(admin_login_required, name='dispatch')
class ActualizarStockEscanerView(View):
    """
    Endpoint AJAX: recibe id del producto y cantidad a sumar al stock.
    """
    def post(self, request):
        try:
            data     = json.loads(request.body)
            prod_id  = data.get('id')
            cantidad = int(data.get('cantidad', 0))
        except (json.JSONDecodeError, ValueError, TypeError):
            return JsonResponse({'status': 'error', 'mensaje': 'Datos inválidos.'})

        if cantidad <= 0:
            return JsonResponse({'status': 'error', 'mensaje': 'La cantidad debe ser mayor a 0.'})

        producto = get_object_or_404(Producto, idProducto=prod_id)
        nuevo_stock = producto.stock + cantidad
        if nuevo_stock > 1000:
            return JsonResponse({'status': 'error', 'mensaje': 'El stock no puede superar 1.000 unidades.'})

        producto.stock = nuevo_stock
        producto.save()
        return JsonResponse({
            'status': 'ok',
            'nombre': producto.nombre,
            'stock_nuevo': producto.stock,
        })


def _consultar_open_food_facts(codigo):
    """Consulta la API pública de Open Food Facts. Retorna el nombre del producto o None."""
    url = f'https://world.openfoodfacts.org/api/v0/product/{codigo}.json'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'SistemaInventario/1.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if data.get('status') == 1:
            product = data.get('product', {})
            nombre = (
                product.get('product_name_es')
                or product.get('product_name')
                or product.get('abbreviated_product_name')
                or ''
            )
            return nombre.strip() if nombre.strip() else None
    except Exception:
        pass
    return None


# ── Alias de vistas ──────────────────────────────────────────────
productos              = ProductosView.as_view()
crear_producto         = CrearProductoView.as_view()
editar_producto        = EditarProductoView.as_view()
eliminar_producto      = EliminarProductoView.as_view()
buscar_codigo_barras   = BuscarCodigoBarrasView.as_view()
actualizar_stock_escaner = ActualizarStockEscanerView.as_view()