"""Vistas para reportes y estadísticas"""
from django.shortcuts import render
from app.decorators import admin_login_required

@admin_login_required
def reportes(request):
    """Vista de reportes del sistema"""
    return render(request, 'Reportes/reportes.html')
