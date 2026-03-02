"""Vista principal del sistema"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ...models import Producto, Cliente, Venta


@login_required
def index(request):
    """Página de inicio con estadísticas generales"""
    try:
        total_productos = Producto.objects.count()
        total_clientes = Cliente.objects.count()
        total_ventas = Venta.objects.count()
    except:
        total_productos = total_clientes = total_ventas = 0
    
    return render(request, "Inicio/index.html", {
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'total_ventas': total_ventas,
    })
