from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import (
    Administrador, Producto, Cliente, Venta, 
    Marca, TipoProductos, unidad_medida
)
from .forms import AdministradorRegistroForm


def index(request):
    return render(request, "base.html")


def productos(request):
    lista_productos = Producto.objects.all().select_related('idMarca', 'idTipo', 'idUnidad')
    
    # Obtener datos para los selects del modal
    marcas = Marca.objects.all()
    tipos = TipoProductos.objects.all()
    unidades = unidad_medida.objects.all()
    
    context = {
        'productos': lista_productos,
        'marcas': marcas,
        'tipos': tipos,
        'unidades': unidades
    }
    
    return render(request, "administrador/productos.html", context)


def crear_producto(request):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.POST.get('nombre')
            precio = request.POST.get('precio')
            stock = request.POST.get('stock')
            id_marca = request.POST.get('idMarca')
            id_tipo = request.POST.get('idTipo')
            id_unidad = request.POST.get('idUnidad')
            
            # Debug: imprimir los valores recibidos
            print(f"Datos recibidos - Nombre: {nombre}, Precio: {precio}, Stock: {stock}")
            print(f"IDs - Marca: {id_marca}, Tipo: {id_tipo}, Unidad: {id_unidad}")
            
            # Crear el producto
            producto = Producto.objects.create(
                nombre=nombre,
                precio=precio,
                stock=stock,
                idMarca_id=id_marca,
                idTipo_id=id_tipo,
                idUnidad_id=id_unidad
            )
            
            messages.success(request, f'Producto "{nombre}" creado exitosamente.')
            return redirect('productos')
            
        except Exception as e:
            print(f"Error completo: {e}")  # Debug: mostrar error en consola
            messages.error(request, f'Error al crear el producto: {str(e)}')
            return redirect('productos')
    
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
            return redirect('productos')
            
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


def clientes(request):
    lista_clientes = Cliente.objects.all()
    return render(request, "clientes.html", {'clientes': lista_clientes})


def ventas(request):
    lista_ventas = Venta.objects.all().select_related('idAdministrador', 'idCliente', 'idProducto')
    return render(request, "ventas.html", {'ventas': lista_ventas})


# ===== REGISTRO DE ADMINISTRADOR =====

def registrar_administrador(request):
    if request.method == 'POST':
        form = AdministradorRegistroForm(request.POST)
        
        if form.is_valid():
            administrador = form.save(commit=False)
            administrador.save()
            
            messages.success(request, '¡Administrador registrado exitosamente!')
            return redirect('inicio')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = AdministradorRegistroForm()
    
    return render(request, 'administrador/registro.html', {'form': form})