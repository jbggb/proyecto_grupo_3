from django.shortcuts import render

def ventas_view(request):
    return render(request, 'ventas/ventas.html')