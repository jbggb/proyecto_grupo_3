from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Administrador
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
            # Crear el administrador sin guardar aún
            administrador = form.save(commit=False)
            
            # Aquí podrías hashear la contraseña si lo deseas
            # from django.contrib.auth.hashers import make_password
            # administrador.contrasena = make_password(form.cleaned_data['contrasena'])
            
            administrador.save()
            
            messages.success(request, '¡Administrador registrado exitosamente!')
            return redirect('inicio')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = AdministradorRegistroForm()
    
    return render(request, 'administrador/registro.html', {'form': form})


# ===== VISTAS BASADAS EN CLASES =====

class ProductoListView(ListView):
    # model = Producto
    template_name = "productos.html"
    context_object_name = 'productos'
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class ProductoCreateView(CreateView):
    template_name = "producto/create.html"
    success_url = reverse_lazy('productos')
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ClienteCreateView(CreateView):
    template_name = "cliente/create.html"
    success_url = reverse_lazy('clientes')


class VentaCreateView(CreateView):
    template_name = "venta/create.html"
    success_url = reverse_lazy('ventas')


class CategoriaCreateView(CreateView):
    template_name = "categoria/create.html"
    success_url = reverse_lazy('productos')
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)