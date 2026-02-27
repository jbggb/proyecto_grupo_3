from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Administrador, Producto, Cliente, Venta, Marca, TipoProductos, unidad_medida
from .forms import AdministradorRegistroForm, ProductoForm, MarcaForm, TipoProductoForm, UnidadMedidaForm


def index(request):
    return render(request, "base.html")


def productos(request):
    lista_productos = Producto.objects.all().select_related('idMarca', 'idTipo', 'idUnidad')
    marcas = Marca.objects.all()
    tipos = TipoProductos.objects.all()
    unidades = unidad_medida.objects.all()
    context = {'productos': lista_productos, 'marcas': marcas, 'tipos': tipos, 'unidades': unidades}
    return render(request, "administrador/productos.html", context)


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            try:
                producto = form.save()
                messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
                return redirect('productos')
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
                return redirect('productos')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('productos')
    return redirect('productos')


def editar_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            try:
                producto = form.save()
                messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
                return redirect('productos')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')
                return redirect('productos')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('productos')
    return redirect('productos')


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    nombre = producto.nombre
    try:
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar el producto: {str(e)}')
    return redirect('productos')


# =============================================
# AJAX: Marca
# =============================================
@require_POST
def crear_marca_ajax(request):
    form = MarcaForm(request.POST)
    if form.is_valid():
        marca = form.save()
        return JsonResponse({'success': True, 'id': marca.idMarca, 'nombre': marca.nombreMarca,
                             'message': f'Marca "{marca.nombreMarca}" creada exitosamente.'})
    errores = [e for field_errors in form.errors.values() for e in field_errors]
    return JsonResponse({'success': False, 'errors': errores}, status=400)


@require_POST
def eliminar_marca_ajax(request, id):
    marca = get_object_or_404(Marca, idMarca=id)
    nombre = marca.nombreMarca
    try:
        if marca.producto_set.exists():
            return JsonResponse({'success': False, 'errors': [f'No se puede eliminar "{nombre}" porque tiene productos asociados.']}, status=400)
        marca.delete()
        return JsonResponse({'success': True, 'message': f'Marca "{nombre}" eliminada exitosamente.'})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': [str(e)]}, status=400)


def listar_marcas_ajax(request):
    items = [{'id': m.idMarca, 'nombre': m.nombreMarca} for m in Marca.objects.all()]
    return JsonResponse({'items': items})


# =============================================
# AJAX: Tipo
# =============================================
@require_POST
def crear_tipo_ajax(request):
    form = TipoProductoForm(request.POST)
    if form.is_valid():
        tipo = form.save()
        return JsonResponse({'success': True, 'id': tipo.idTipo, 'nombre': tipo.nombre_tipo,
                             'message': f'Tipo "{tipo.nombre_tipo}" creado exitosamente.'})
    errores = [e for field_errors in form.errors.values() for e in field_errors]
    return JsonResponse({'success': False, 'errors': errores}, status=400)


@require_POST
def eliminar_tipo_ajax(request, id):
    tipo = get_object_or_404(TipoProductos, idTipo=id)
    nombre = tipo.nombre_tipo
    try:
        if tipo.producto_set.exists():
            return JsonResponse({'success': False, 'errors': [f'No se puede eliminar "{nombre}" porque tiene productos asociados.']}, status=400)
        tipo.delete()
        return JsonResponse({'success': True, 'message': f'Tipo "{nombre}" eliminado exitosamente.'})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': [str(e)]}, status=400)


def listar_tipos_ajax(request):
    items = [{'id': t.idTipo, 'nombre': t.nombre_tipo} for t in TipoProductos.objects.all()]
    return JsonResponse({'items': items})


# =============================================
# AJAX: Unidad
# =============================================
@require_POST
def crear_unidad_ajax(request):
    form = UnidadMedidaForm(request.POST)
    if form.is_valid():
        unidad = form.save()
        return JsonResponse({'success': True, 'id': unidad.idUnidad,
                             'nombre': f'{unidad.nombre_unidad} ({unidad.abreviatura})',
                             'message': f'Unidad "{unidad.nombre_unidad}" creada exitosamente.'})
    errores = [e for field_errors in form.errors.values() for e in field_errors]
    return JsonResponse({'success': False, 'errors': errores}, status=400)


@require_POST
def eliminar_unidad_ajax(request, id):
    unidad = get_object_or_404(unidad_medida, idUnidad=id)
    nombre = unidad.nombre_unidad
    try:
        if unidad.producto_set.exists():
            return JsonResponse({'success': False, 'errors': [f'No se puede eliminar "{nombre}" porque tiene productos asociados.']}, status=400)
        unidad.delete()
        return JsonResponse({'success': True, 'message': f'Unidad "{nombre}" eliminada exitosamente.'})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': [str(e)]}, status=400)


def listar_unidades_ajax(request):
    items = [{'id': u.idUnidad, 'nombre': f'{u.nombre_unidad} ({u.abreviatura})'} for u in unidad_medida.objects.all()]
    return JsonResponse({'items': items})


def clientes(request):
    return render(request, "clientes.html", {'clientes': Cliente.objects.all()})


def ventas(request):
    lista_ventas = Venta.objects.all().select_related('idAdministrador', 'idCliente', 'idProducto')
    return render(request, "ventas.html", {'ventas': lista_ventas})


def registrar_administrador(request):
    if request.method == 'POST':
        form = AdministradorRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Administrador registrado exitosamente!')
            return redirect('inicio')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = AdministradorRegistroForm()
    return render(request, 'administrador/registro.html', {'form': form})


def reportes(request):
    return render(request, 'administrador/reportes.html')