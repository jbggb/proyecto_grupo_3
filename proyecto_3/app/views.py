from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import (
    Administrador, Producto, Cliente, Venta, 
    Marca, TipoProductos, unidad_medida
)
from .forms import AdministradorRegistroForm, ProductoForm


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
        # Usar el formulario con validaciones
        form = ProductoForm(request.POST)
        
        if form.is_valid():
            try:
                # Guardar el producto usando el formulario validado
                producto = form.save()
                messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
                return redirect('productos')
            except Exception as e:
                print(f"Error al guardar: {e}")
                messages.error(request, f'Error al crear el producto: {str(e)}')
                return redirect('productos')
        else:
            # Mostrar errores de validación
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
            return redirect('productos')
    
    return redirect('productos')


def editar_producto(request, id):
    producto = get_object_or_404(Producto, idProducto=id)
    
    if request.method == 'POST':
        # Usar el formulario con validaciones para editar
        form = ProductoForm(request.POST, instance=producto)
        
        if form.is_valid():
            try:
                producto = form.save()
                messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
                return redirect('productos')
            except Exception as e:
                print(f"Error al actualizar: {e}")
                messages.error(request, f'Error al actualizar el producto: {str(e)}')
                return redirect('productos')
        else:
            # Mostrar errores de validación
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
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

def reportes(request):
    return render(request, 'administrador/reportes.html')