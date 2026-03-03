from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import Producto, Marca, TipoProductos, unidad_medida
import re


def productos(request):
    query = request.GET.get('q', '')
    lista = Producto.objects.all()
    if query:
        lista = lista.filter(nombre__icontains=query)
    marcas = Marca.objects.all()
    tipos = TipoProductos.objects.all()
    unidades = unidad_medida.objects.all()
    return render(request, 'Productos/productos.html', {
        'productos': lista,
        'marcas': marcas,
        'tipos': tipos,
        'unidades': unidades,
    })


def crear_producto(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre', '').strip()
            precio = request.POST.get('precio', '').strip()
            stock = request.POST.get('stock', '').strip()
            idMarca = request.POST.get('idMarca')
            idTipo = request.POST.get('idTipo')
            idUnidad = request.POST.get('idUnidad')

            if not nombre:
                messages.error(request, 'El nombre es obligatorio.')
                return redirect('productos')

            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
                messages.error(request, 'El nombre solo puede contener letras y espacios.')
                return redirect('productos')

            if Marca.objects.filter(nombreMarca__iexact=nombre).exists():
                messages.error(request, f'"{nombre}" ya existe como Marca. Use un nombre diferente.')
                return redirect('productos')

            if TipoProductos.objects.filter(nombre_tipo__iexact=nombre).exists():
                messages.error(request, f'"{nombre}" ya existe como Tipo de producto. Use un nombre diferente.')
                return redirect('productos')

            if unidad_medida.objects.filter(nombre_unidad__iexact=nombre).exists():
                messages.error(request, f'"{nombre}" ya existe como Unidad de medida. Use un nombre diferente.')
                return redirect('productos')

            if Producto.objects.filter(nombre__iexact=nombre, idMarca=idMarca, idTipo=idTipo).exists():
                messages.error(request, f'Ya existe un producto llamado "{nombre}" con esa marca y tipo.')
                return redirect('productos')

            if not precio.isdigit() or int(precio) < 1 or int(precio) > 800000:
                messages.error(request, 'El precio debe ser un numero entre 1 y 800.000.')
                messages.error(request, 'El precio no puede ser 0 ni negativo, y no puede superar 800.000.')
                return redirect('productos')

            if not stock.isdigit() or int(stock) < 0 or int(stock) > 1000:
                messages.error(request, 'El stock debe ser un numero entre 0 y 1.000.')
                return redirect('productos')

            Producto.objects.create(
                nombre=nombre,
                precio=precio,
                stock=stock,
                idMarca=get_object_or_404(Marca, idMarca=idMarca),
                idTipo=get_object_or_404(TipoProductos, idTipo=idTipo),
                idUnidad=get_object_or_404(unidad_medida, idUnidad=idUnidad),
            )
            messages.success(request, f'Producto "{nombre}" creado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el producto: {str(e)}')
    return redirect('productos')


def editar_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        idMarca = request.POST.get('idMarca')
        idTipo = request.POST.get('idTipo')

        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$', nombre):
            messages.error(request, 'El nombre solo puede contener letras y espacios.')
            return redirect('productos')

        if Marca.objects.filter(nombreMarca__iexact=nombre).exists():
            messages.error(request, f'"{nombre}" ya existe como Marca. Use un nombre diferente.')
            return redirect('productos')

        if TipoProductos.objects.filter(nombre_tipo__iexact=nombre).exists():
            messages.error(request, f'"{nombre}" ya existe como Tipo de producto. Use un nombre diferente.')
            return redirect('productos')

        if unidad_medida.objects.filter(nombre_unidad__iexact=nombre).exists():
            messages.error(request, f'"{nombre}" ya existe como Unidad de medida. Use un nombre diferente.')
            return redirect('productos')

        if Producto.objects.filter(nombre__iexact=nombre, idMarca=idMarca, idTipo=idTipo).exclude(idProducto=id).exists():
            messages.error(request, f'Ya existe un producto llamado "{nombre}" con esa marca y tipo.')
            return redirect('productos')

        producto.nombre = nombre
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')
        producto.idMarca = get_object_or_404(Marca, idMarca=idMarca)
        producto.idTipo = get_object_or_404(TipoProductos, idTipo=idTipo)
        producto.idUnidad = get_object_or_404(unidad_medida, idUnidad=request.POST.get('idUnidad'))
        producto.save()
        messages.success(request, f'Producto "{nombre}" actualizado correctamente.')
    return redirect('productos')


def eliminar_producto(request, id):
    try:
        producto = get_object_or_404(Producto, idProducto=id)
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado correctamente.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    return redirect('productos')