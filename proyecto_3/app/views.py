import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.utils import timezone
from django.db.models import Sum
from .models import (
    Administrador, Producto, Cliente, Venta, DetalleVenta,
    Marca, TipoProductos, unidad_medida, Proveedor, Compra
)
from .forms import AdministradorRegistroForm


# ===== INICIO =====
@login_required
def index(request):
    try:
        total_productos = Producto.objects.count()
        total_clientes = Cliente.objects.count()
        total_ventas = Venta.objects.count()
    except:
        total_productos = total_clientes = total_ventas = 0
    return render(request, "index.html", {
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
    })


# ===== PRODUCTOS =====
@login_required
def productos(request):
    context = {
        'productos': Producto.objects.all().select_related('idMarca', 'idTipo', 'idUnidad'),
        'marcas': Marca.objects.all(),
        'tipos': TipoProductos.objects.all(),
        'unidades': unidad_medida.objects.all(),
    }
    return render(request, "administrador/productos.html", context)


@login_required
def crear_producto(request):
    if request.method == 'POST':
        try:
            precio = request.POST.get('precio', '0')
            if not precio.isdigit() or int(precio) > 99999999:
                messages.error(request, 'El precio debe ser un número entero entre 0 y 99,999,999.')
                return redirect('productos')
            Producto.objects.create(
                nombre=request.POST.get('nombre'),
                precio=int(precio),
                stock=request.POST.get('stock'),
                idMarca_id=request.POST.get('idMarca'),
                idTipo_id=request.POST.get('idTipo'),
                idUnidad_id=request.POST.get('idUnidad'),
            )
            messages.success(request, f'Producto "{request.POST.get("nombre")}" creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el producto: {str(e)}')
    return redirect('productos')


@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    if request.method == 'POST':
        try:
            producto.nombre = request.POST.get('nombre')
            producto.precio = request.POST.get('precio')
            producto.stock = request.POST.get('stock')
            producto.idMarca_id = request.POST.get('idMarca')
            producto.idTipo_id = request.POST.get('idTipo')
            producto.idUnidad_id = request.POST.get('idUnidad')
            producto.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
    return redirect('productos')


@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    try:
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar: {str(e)}')
    return redirect('productos')


# ===== AJAX: MARCAS =====
@login_required
def crear_marca_ajax(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreMarca', '').strip()
        if not nombre:
            return JsonResponse({'success': False, 'errors': ['El nombre es obligatorio.']})
        if Marca.objects.filter(nombreMarca__iexact=nombre).exists():
            return JsonResponse({'success': False, 'errors': ['Ya existe una marca con ese nombre.']})
        marca = Marca.objects.create(nombreMarca=nombre)
        return JsonResponse({'success': True, 'id': marca.idMarca, 'nombre': marca.nombreMarca, 'message': f'Marca "{nombre}" creada.'})
    return JsonResponse({'success': False, 'errors': ['Método no permitido.']})


@login_required
def eliminar_marca_ajax(request, id):
    if request.method == 'POST':
        marca = get_object_or_404(Marca, idMarca=id)
        if Producto.objects.filter(idMarca=marca).exists():
            return JsonResponse({'success': False, 'errors': ['No se puede eliminar: tiene productos asociados.']})
        marca.delete()
        return JsonResponse({'success': True, 'message': 'Marca eliminada.'})
    return JsonResponse({'success': False, 'errors': ['Método no permitido.']})


@login_required
def listar_marcas_ajax(request):
    items = [{'id': m.idMarca, 'nombre': m.nombreMarca} for m in Marca.objects.all()]
    return JsonResponse({'items': items})


# ===== AJAX: TIPOS =====
@login_required
def crear_tipo_ajax(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_tipo', '').strip()
        if not nombre:
            return JsonResponse({'success': False, 'errors': ['El nombre es obligatorio.']})
        if TipoProductos.objects.filter(nombre_tipo__iexact=nombre).exists():
            return JsonResponse({'success': False, 'errors': ['Ya existe un tipo con ese nombre.']})
        tipo = TipoProductos.objects.create(nombre_tipo=nombre, descripcion='')
        return JsonResponse({'success': True, 'id': tipo.idTipo, 'nombre': tipo.nombre_tipo, 'message': f'Tipo "{nombre}" creado.'})
    return JsonResponse({'success': False, 'errors': ['Método no permitido.']})


@login_required
def eliminar_tipo_ajax(request, id):
    if request.method == 'POST':
        tipo = get_object_or_404(TipoProductos, idTipo=id)
        if Producto.objects.filter(idTipo=tipo).exists():
            return JsonResponse({'success': False, 'errors': ['No se puede eliminar: tiene productos asociados.']})
        tipo.delete()
        return JsonResponse({'success': True, 'message': 'Tipo eliminado.'})
    return JsonResponse({'success': False, 'errors': ['Método no permitido.']})


@login_required
def listar_tipos_ajax(request):
    items = [{'id': t.idTipo, 'nombre': t.nombre_tipo} for t in TipoProductos.objects.all()]
    return JsonResponse({'items': items})


# ===== AJAX: UNIDADES =====
@login_required
def crear_unidad_ajax(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_unidad', '').strip()
        abrev = request.POST.get('abreviatura', '-').strip() or '-'
        if not nombre:
            return JsonResponse({'success': False, 'errors': ['El nombre es obligatorio.']})
        unidad = unidad_medida.objects.create(nombre_unidad=nombre, abreviatura=abrev)
        return JsonResponse({'success': True, 'id': unidad.idUnidad, 'nombre': f'{unidad.nombre_unidad} ({unidad.abreviatura})', 'message': f'Unidad "{nombre}" creada.'})
    return JsonResponse({'success': False, 'errors': ['Método no permitido.']})


@login_required
def eliminar_unidad_ajax(request, id):
    if request.method == 'POST':
        unidad = get_object_or_404(unidad_medida, idUnidad=id)
        if Producto.objects.filter(idUnidad=unidad).exists():
            return JsonResponse({'success': False, 'errors': ['No se puede eliminar: tiene productos asociados.']})
        unidad.delete()
        return JsonResponse({'success': True, 'message': 'Unidad eliminada.'})
    return JsonResponse({'success': False, 'errors': ['Método no permitido.']})


@login_required
def listar_unidades_ajax(request):
    items = [{'id': u.idUnidad, 'nombre': f'{u.nombre_unidad} ({u.abreviatura})'} for u in unidad_medida.objects.all()]
    return JsonResponse({'items': items})


# ===== CLIENTES =====
@login_required
def clientes(request):
    return render(request, "cliente/clientes.html", {'clientes': Cliente.objects.all()})

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if Cliente.objects.filter(documento=data['documento']).exists():
                return JsonResponse({'ok': False, 'error': 'Ya existe un cliente con ese documento.'})
            if Cliente.objects.filter(email=data['email']).exists():
                return JsonResponse({'ok': False, 'error': 'Ya existe un cliente con ese email.'})
            Cliente.objects.create(
                nombre=data['nombre'],
                documento=data['documento'],
                telefono=data['telefono'],
                email=data['email'],
                direccion=data['direccion'],
                estado=data['estado'],
            )
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})


@login_required
def editar_cliente(request, id):
    if request.method == 'POST':
        try:
            cliente = get_object_or_404(Cliente, id=id)
            data = json.loads(request.body)
            if Cliente.objects.filter(documento=data['documento']).exclude(id=id).exists():
                return JsonResponse({'ok': False, 'error': 'Ya existe otro cliente con ese documento.'})
            if Cliente.objects.filter(email=data['email']).exclude(id=id).exists():
                return JsonResponse({'ok': False, 'error': 'Ya existe otro cliente con ese email.'})
            cliente.nombre = data['nombre']
            cliente.documento = data['documento']
            cliente.telefono = data['telefono']
            cliente.email = data['email']
            cliente.direccion = data['direccion']
            cliente.estado = data['estado']
            cliente.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})


@login_required
def eliminar_cliente(request, id):
    if request.method == 'POST':
        try:
            cliente = get_object_or_404(Cliente, id=id)
            cliente.delete()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})


@login_required
def clientes_json(request):
    lista = list(Cliente.objects.all().values(
        'id', 'nombre', 'documento', 'telefono', 'email', 'direccion', 'estado'
    ))
    return JsonResponse({'clientes': lista})



# ===== VENTAS (Ricardo) =====
@login_required
def ventas(request):
    lista_ventas = Venta.objects.prefetch_related('detalles').all()
    return render(request, "Ventas/Ventas.html", {'ventas': lista_ventas})


@login_required
def crear_venta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = data.get('cliente', '').strip()
            estado = data.get('estado', 'pendiente')
            total = data.get('total', 0)
            productos_lista = data.get('productos', [])

            errores = {}
            if not cliente or len(cliente) < 3:
                errores['cliente'] = ['El nombre debe tener al menos 3 caracteres.']
            if not productos_lista:
                errores['productos'] = ['Debe agregar al menos un producto.']
            if errores:
                return JsonResponse({'ok': False, 'errores': errores})

            venta = Venta.objects.create(cliente=cliente, estado=estado, total=total)
            for p in productos_lista:
                DetalleVenta.objects.create(
                    venta=venta,
                    producto_nombre=p['nombre'],
                    precio=p['precio'],
                    cantidad=p['cantidad'],
                )
            return JsonResponse({'ok': True, 'id': venta.id})
        except Exception as e:
            return JsonResponse({'ok': False, 'errores': {'general': [str(e)]}})
    return JsonResponse({'ok': False, 'errores': {'general': ['Método no permitido.']}})


@login_required
def detalle_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    productos_lista = [
        {'nombre': d.producto_nombre, 'precio': float(d.precio), 'cantidad': d.cantidad}
        for d in venta.detalle_venta_set.all()
    ]
    return JsonResponse({
        'id': venta.id,
        'cliente': venta.cliente,
        'fecha': venta.fecha.strftime('%d/%m/%Y %H:%M'),
        'estado': venta.estado,
        'total': float(venta.total),
        'productos': productos_lista,
    })


@login_required
def editar_venta(request, id):
    if request.method == 'POST':
        try:
            venta = get_object_or_404(Venta, id=id)
            data = json.loads(request.body)
            cliente = data.get('cliente', '').strip()
            estado = data.get('estado', 'pendiente')
            total = data.get('total', 0)
            productos_lista = data.get('productos', [])

            errores = {}
            if not cliente:
                errores['cliente'] = ['El nombre es obligatorio.']
            if not productos_lista:
                errores['productos'] = ['Debe haber al menos un producto.']
            if errores:
                return JsonResponse({'ok': False, 'errores': errores})

            venta.cliente = cliente
            venta.estado = estado
            venta.total = total
            venta.save()

            venta.detalle_venta_set.all().delete()
            for p in productos_lista:
                DetalleVenta.objects.create(
                    venta=venta,
                    producto_nombre=p['nombre'],
                    precio=p['precio'],
                    cantidad=p['cantidad'],
                )
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'errores': {'general': [str(e)]}})
    return JsonResponse({'ok': False, 'errores': {'general': ['Método no permitido.']}})


@login_required
def completar_venta(request, id):
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=id)
        venta.estado = 'completada'
        venta.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False})


@login_required
def eliminar_venta(request, id):
    if request.method == 'POST':
        venta = get_object_or_404(Venta, id=id)
        venta.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False})


@login_required
def estadisticas_ventas(request):
    hoy = timezone.now().date()
    ventas_hoy = Venta.objects.filter(fecha__date=hoy).aggregate(total=Sum('total'))['total'] or 0
    total_mes = Venta.objects.filter(fecha__year=hoy.year, fecha__month=hoy.month).aggregate(total=Sum('total'))['total'] or 0
    total_ventas = Venta.objects.count()
    return JsonResponse({
        'ventas_hoy': float(ventas_hoy),
        'total_mes': float(total_mes),
        'total_ventas': total_ventas,
    })


# ===== PROVEEDORES =====
@login_required
def proveedores(request):
    return render(request, 'proveedores/proveedores.html')

@login_required
def proveedores_json(request):
    lista = list(Proveedor.objects.all().values(
        'id', 'nombre', 'telefono', 'email', 'envio', 'fechaRegistro'
    ))
    return JsonResponse({'proveedores': lista})

@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if Proveedor.objects.filter(email=data['email']).exists():
                return JsonResponse({'ok': False, 'error': 'Ya existe un proveedor con ese email.'})
            Proveedor.objects.create(
                nombre=data['nombre'],
                telefono=data['telefono'],
                email=data['email'],
                envio=int(data.get('envio', 0)),
            )
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})

@login_required
def editar_proveedor(request, id):
    if request.method == 'POST':
        try:
            proveedor = get_object_or_404(Proveedor, id=id)
            data = json.loads(request.body)
            if Proveedor.objects.filter(email=data['email']).exclude(id=id).exists():
                return JsonResponse({'ok': False, 'error': 'Ya existe otro proveedor con ese email.'})
            proveedor.nombre = data['nombre']
            proveedor.telefono = data['telefono']
            proveedor.email = data['email']
            proveedor.envio = int(data.get('envio', 0))
            proveedor.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})

@login_required
def eliminar_proveedor(request, id):
    if request.method == 'POST':
        try:
            proveedor = get_object_or_404(Proveedor, id=id)
            proveedor.delete()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})


# ===== LOGIN / LOGOUT / REGISTRO =====
def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('inicio')
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')


def registrar_administrador(request):
    if request.method == 'POST':
        form = AdministradorRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Administrador registrado exitosamente!')
            return redirect('inicio')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = AdministradorRegistroForm()
    return render(request, 'registro.html', {'form': form})


# ===== ADMINISTRADOR (diego) =====
@login_required
def admin_productos(request):
    return render(request, 'administrador/productos.html', {
        'productos': Producto.objects.all().select_related('idMarca', 'idTipo', 'idUnidad'),
        'marcas': Marca.objects.all(),
    })


@login_required
def admin_registro(request):
    if request.method == 'POST':
        form = AdministradorRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('inicio')
    else:
        form = AdministradorRegistroForm()
    return render(request, 'administrador/registro.html', {'form': form})


@login_required
def reportes(request):
    return render(request, 'administrador/reportes.html')


# ===== ADMINISTRADORES JSON =====
@login_required
def administradores_json(request):
    lista = list(Administrador.objects.all().values('id', 'nombre'))
    return JsonResponse({'administradores': lista})

# ===== COMPRAS (MOJICA) =====
@login_required
def compras(request):
    lista_compras = Compra.objects.select_related('Administrador', 'Producto', 'Proveedor').all().order_by('-fecha')
    proveedores = Proveedor.objects.all()
    productos = Producto.objects.all()
    administradores = Administrador.objects.all()
    return render(request, 'Compras/Compras.html', {
        'compras': lista_compras,
        'proveedores': proveedores,
        'productos': productos,
        'administradores': administradores,
    })

def _get_or_create_admin():
    """Obtiene el primer administrador disponible, o lo crea desde auth_user."""
    from django.contrib.auth.models import User
    from datetime import date
    admin = Administrador.objects.first()
    if not admin:
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if user:
            admin = Administrador.objects.create(
                nombre=user.get_full_name() or user.username,
                usuario=user.username,
                contrasena=user.password,
                email=user.email or f'{user.username}@admin.com',
                fechaRegistro=date.today(),
            )
    return admin

@login_required
def crear_compra(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            admin = _get_or_create_admin()
            if not admin:
                return JsonResponse({'ok': False, 'error': 'No hay administradores registrados en el sistema.'})
            Compra.objects.create(
                fecha=data['fecha'],
                estado=data['estado'],
                Administrador=admin,
                Producto_id=data['producto_id'],
                Proveedor_id=data['proveedor_id'],
            )
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})

@login_required
def editar_compra(request, id):
    if request.method == 'POST':
        try:
            compra = get_object_or_404(Compra, id=id)
            data = json.loads(request.body)
            admin = _get_or_create_admin()
            if not admin:
                return JsonResponse({'ok': False, 'error': 'No hay administradores registrados en el sistema.'})
            compra.fecha = data['fecha']
            compra.estado = data['estado']
            compra.Administrador = admin
            compra.Producto_id = data['producto_id']
            compra.Proveedor_id = data['proveedor_id']
            compra.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})

@login_required
def eliminar_compra(request, id):
    if request.method == 'POST':
        try:
            compra = get_object_or_404(Compra, id=id)
            compra.delete()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})

@login_required
def compras_json(request):
    lista = []
    for c in Compra.objects.select_related('Administrador', 'Producto', 'Proveedor').all().order_by('-fecha'):
        lista.append({
            'id': c.id,
            'fecha': str(c.fecha),
            'estado': c.estado,
            'administrador': c.Administrador.nombre if c.Administrador else '',
            'administrador_id': c.Administrador_id,
            'producto': c.Producto.nombre if c.Producto else '',
            'producto_id': c.Producto_id,
            'proveedor': c.Proveedor.nombre if c.Proveedor else '',
            'proveedor_id': c.Proveedor_id,
        })
    return JsonResponse({'compras': lista})

@login_required
def productos_json(request):
    productos = Producto.objects.all().values('idProducto', 'nombre', 'precio', 'stock')
    lista = [{'id': p['idProducto'], 'nombre': p['nombre'], 'precio': float(p['precio']), 'stock': p['stock']} for p in productos]
    return JsonResponse({'productos': lista})