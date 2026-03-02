"""Vistas para gestión de productos"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...models import Producto, Marca, TipoProductos, unidad_medida


@login_required
def productos(request):
    """Lista de productos con filtros"""
    context = {
        'productos': Producto.objects.all().select_related('idMarca', 'idTipo', 'idUnidad'),
        'marcas': Marca.objects.all(),
        'tipos': TipoProductos.objects.all(),
        'unidades': unidad_medida.objects.all(),
    }
    return render(request, "Productos/productos.html", context)


@login_required
def crear_producto(request):
    """Crear un nuevo producto"""
    if request.method == 'POST':
        try:
            # Validar nombre
            nombre = request.POST.get('nombre', '').strip()
            if not nombre or len(nombre) < 3:
                messages.error(request, 'El nombre debe tener al menos 3 caracteres.')
                return redirect('productos')
            
            # Validar precio
            precio = request.POST.get('precio', '0')
            if not precio.isdigit():
                messages.error(request, 'El precio debe ser un número entero.')
                return redirect('productos')
            precio = int(precio)
            if precio < 1 or precio > 99999999:
                messages.error(request, 'El precio debe estar entre 1 y 99,999,999.')
                return redirect('productos')
            
            # Validar stock
            stock = request.POST.get('stock', '0')
            if not stock.isdigit():
                messages.error(request, 'El stock debe ser un número entero.')
                return redirect('productos')
            stock = int(stock)
            if stock < 0 or stock > 999999:
                messages.error(request, 'El stock debe estar entre 0 y 999,999.')
                return redirect('productos')
            
            # Validar marca, tipo y unidad
            marca_id = request.POST.get('idMarca')
            tipo_id = request.POST.get('idTipo')
            unidad_id = request.POST.get('idUnidad')
            
            if not marca_id or not tipo_id or not unidad_id:
                messages.error(request, 'Debe seleccionar marca, tipo y unidad.')
                return redirect('productos')
            
            # Crear producto
            Producto.objects.create(
                nombre=nombre,
                precio=precio,
                stock=stock,
                idMarca_id=marca_id,
                idTipo_id=tipo_id,
                idUnidad_id=unidad_id,
            )
            messages.success(request, f'Producto "{nombre}" creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el producto: {str(e)}')
    
    return redirect('productos')


@login_required
def editar_producto(request, id):
    """Editar un producto existente"""
    producto = get_object_or_404(Producto, idProducto=id)
    
    if request.method == 'POST':
        try:
            # Validar nombre
            nombre = request.POST.get('nombre', '').strip()
            if not nombre or len(nombre) < 3:
                messages.error(request, 'El nombre debe tener al menos 3 caracteres.')
                return redirect('productos')
            
            # Validar precio
            precio = request.POST.get('precio', '0')
            if not precio.isdigit():
                messages.error(request, 'El precio debe ser un número entero.')
                return redirect('productos')
            precio = int(precio)
            if precio < 1 or precio > 99999999:
                messages.error(request, 'El precio debe estar entre 1 y 99,999,999.')
                return redirect('productos')
            
            # Validar stock
            stock = request.POST.get('stock', '0')
            if not stock.isdigit():
                messages.error(request, 'El stock debe ser un número entero.')
                return redirect('productos')
            stock = int(stock)
            if stock < 0 or stock > 999999:
                messages.error(request, 'El stock debe estar entre 0 y 999,999.')
                return redirect('productos')
            
            # Validar marca, tipo y unidad
            marca_id = request.POST.get('idMarca')
            tipo_id = request.POST.get('idTipo')
            unidad_id = request.POST.get('idUnidad')
            
            if not marca_id or not tipo_id or not unidad_id:
                messages.error(request, 'Debe seleccionar marca, tipo y unidad.')
                return redirect('productos')
            
            # Actualizar producto
            producto.nombre = nombre
            producto.precio = precio
            producto.stock = stock
            producto.idMarca_id = marca_id
            producto.idTipo_id = tipo_id
            producto.idUnidad_id = unidad_id
            producto.save()
            
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
    
    return redirect('productos')


@login_required
def eliminar_producto(request, id):
    """Eliminar un producto"""
    producto = get_object_or_404(Producto, idProducto=id)
    
    try:
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar: {str(e)}')
    
    return redirect('productos')


@login_required
def admin_productos(request):
    """Vista de administración de productos"""
    return render(request, 'Productos/productos.html', {
        'productos': Producto.objects.all().select_related('idMarca', 'idTipo', 'idUnidad'),
        'marcas': Marca.objects.all(),
    })


@login_required
def productos_json(request):
    """Lista de productos en formato JSON"""
    from django.http import JsonResponse
    productos_qs = Producto.objects.all().values('idProducto', 'nombre', 'precio', 'stock')
    lista = [{'id': p['idProducto'], 'nombre': p['nombre'], 'precio': float(p['precio']), 'stock': p['stock']} for p in productos_qs]
    return JsonResponse({'productos': lista})
