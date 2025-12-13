from django.shortcuts import render

def index(request):
    return render(request, "base.html")

def productos(request):
    return render(request, "productos.html")

def clientes(request):
    return render(request, "clientes.html")

def ventas(request):
    return render(request, "ventas.html")