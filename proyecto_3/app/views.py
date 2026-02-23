from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import (Administrador, Cliente, Marca, TipoProductos,
                     unidad_medida, Producto, Proveedor, Venta, Pedidos, compra)
from .forms import AdministradorRegistroForm


def index(request):
    return render(request, "base.html")

def productos(request):
    return render(request, "productos.html")

def clientes(request):
    return render(request, "cliente/clientes.html")

def ventas(request):
    return render(request, "ventas.html")


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


# ===== PRODUCTOS =====

class ProductoListView(ListView):
    model = Producto
    template_name = "productos.html"
    context_object_name = 'productos'


class ProductoCreateView(CreateView):
    model = Producto
    fields = ['idTipo', 'idMarca', 'idUnidad', 'nombre', 'precio', 'stock']
    template_name = "producto/create.html"
    success_url = reverse_lazy('productos')


# ===== CLIENTES =====

class ClienteCreateView(CreateView):
    model = Cliente
    fields = ['nombre', 'telefono', 'email']
    template_name = "cliente/create.html"
    success_url = reverse_lazy('clientes')


# ===== VENTAS =====

class VentaCreateView(CreateView):
    model = Venta
    fields = ['idAdministrador', 'idCliente', 'idProducto', 'fechaVenta', 'totalVenta']
    template_name = "venta/create.html"
    success_url = reverse_lazy('ventas')


# ===== CATEGORIAS =====

class CategoriaCreateView(CreateView):
    model = TipoProductos
    fields = ['nombre_tipo', 'descripcion']
    template_name = "categoria/create.html"
    success_url = reverse_lazy('productos')


# ===== COMPRAS =====

class ComprasListView(ListView):
    model = compra
    template_name = "compras/Compras.html"
    context_object_name = "compras"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proveedores']     = Proveedor.objects.all()
        context['productos']       = Producto.objects.all()
        context['administradores'] = Administrador.objects.all()
        return context


class comprasCreateview(CreateView):
    model = compra
    fields = ['Administrador', 'Proveedor', 'Producto',
              'fecha_compra', 'totalcompra', 'estado']
    template_name = "compras/Compras.html"
    success_url = reverse_lazy('compras')


class ComprasUpdateView(UpdateView):
    model = compra
    fields = ['Administrador', 'Proveedor', 'Producto',
              'fecha_compra', 'totalcompra', 'estado']
    template_name = "compras/Compras.html"
    success_url = reverse_lazy('compras')


class ComprasDeleteView(DeleteView):
    model = compra
    success_url = reverse_lazy('compras')