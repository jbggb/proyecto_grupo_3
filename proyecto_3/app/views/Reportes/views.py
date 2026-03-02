"""Vistas para reportes y estadísticas"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def reportes(request):
    """Vista de reportes del sistema"""
    return render(request, 'Reportes/reportes.html')
