from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import (
    Administrador, Producto, Cliente, Venta,
    Marca, TipoProductos, unidad_medida, Proveedor
)
from .forms import AdministradorRegistroForm


# ===== INICIO =====
def index(request):
    try:
        total_productos = Producto.objects.count()
        total_clientes = Cliente.objects.count()
        total_ventas = Venta.objects.count()
    except:
        total_productos = 0
        total_clientes = 0
        total_ventas = 0

    context = {
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
    }
    return render(request, "index.html", context)


# ===== PRODUCTOS =====
def productos(request):
    lista_productos = Producto.objects.all().select_related('idMarca', 'idTipo', 'idUnidad')
    marcas = Marca.objects.all()
    tipos = TipoProductos.objects.all()
    unidades = unidad_medida.objects.all()
    context = {
        'productos': lista_productos,
        'marcas': marcas,
        'tipos': tipos,
        'unidades': unidades
    }
    return render(request, "Productos/productos.html", context)


def crear_producto(request):
    if request.method == 'POST':
        try:
            nombre = request.POST.get('nombre')
            precio = request.POST.get('precio')
            stock = request.POST.get('stock')
            id_marca = request.POST.get('idMarca')
            id_tipo = request.POST.get('idTipo')
            id_unidad = request.POST.get('idUnidad')
            Producto.objects.create(
                nombre=nombre, precio=precio, stock=stock,
                idMarca_id=id_marca, idTipo_id=id_tipo, idUnidad_id=id_unidad
            )
            messages.success(request, f'Producto "{nombre}" creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el producto: {str(e)}')
    return redirect('productos')


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
            messages.error(request, f'Error al actualizar el producto: {str(e)}')
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


# ===== CLIENTES =====
def clientes(request):
    lista_clientes = Cliente.objects.all()
    return render(request, "cliente/clientes.html", {'clientes': lista_clientes})


# ===== VENTAS =====
def ventas(request):
    lista_ventas = Venta.objects.all().select_related('idAdministrador', 'idCliente', 'idProducto')
    return render(request, "Ventas.html", {'ventas': lista_ventas})


# ===== PROVEEDORES =====
from django.core import serializers

def proveedores(request):
    lista_proveedores = Proveedor.objects.all().select_related('idTipo', 'idProducto')
    lista_productos = Producto.objects.all()
    lista_tipos = TipoProductos.objects.all()
    
    # Serializar para el JS
    productos_json = serializers.serialize('json', lista_productos, fields=['nombre'])
    tipos_json = serializers.serialize('json', lista_tipos, fields=['nombre_tipo'])
    
    context = {
        'proveedores': lista_proveedores,
        'productos': lista_productos,
        'tipos': lista_tipos,
        'productos_json': productos_json,
        'tipos_json': tipos_json,
    }
    return render(request, 'proveedores/proveedores.html', context)


def crear_proveedor(request):
    if request.method == 'POST':
        try:
            Proveedor.objects.create(
                nombre=request.POST.get('nombre'),
                telefono=request.POST.get('telefono'),
                email=request.POST.get('email'),
                idTipo_id=request.POST.get('idTipo'),
                idProducto_id=request.POST.get('idProducto'),
                stock=request.POST.get('stock'),
                envio=request.POST.get('envio') == 'True',
            )
            messages.success(request, 'Proveedor registrado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return redirect('proveedores')


def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        try:
            proveedor.nombre = request.POST.get('nombre')
            proveedor.telefono = request.POST.get('telefono')
            proveedor.email = request.POST.get('email')
            proveedor.idTipo_id = request.POST.get('idTipo')
            proveedor.idProducto_id = request.POST.get('idProducto')
            proveedor.stock = request.POST.get('stock')
            proveedor.envio = request.POST.get('envio') == 'True'
            proveedor.save()
            messages.success(request, f'Proveedor "{proveedor.nombre}" actualizado.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return redirect('proveedores')


def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    try:
        nombre = proveedor.nombre
        proveedor.delete()
        messages.success(request, f'Proveedor "{nombre}" eliminado.')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    return redirect('proveedores')


# ===== REGISTRO DE ADMINISTRADOR =====
def registrar_administrador(request):
    if request.method == 'POST':
        form = AdministradorRegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Administrador registrado exitosamente!')
            return redirect('inicio')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = AdministradorRegistroForm()
    return render(request, 'registro.html', {'form': form})


# ===== LOGIN =====
def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html')


# ===== LOGOUT =====
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')