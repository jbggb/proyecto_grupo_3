from django.urls import path
from . import views

urlpatterns = [
    path('', views.ventas_view, name='ventas'),
    path('crear/', views.crear_venta, name='crear_venta'),
    path('detalle/<int:ventaId>/', views.detalle_venta_view, name='detalle_venta'),
    path('completar/<int:ventaId>/', views.completar_venta_view, name='completar_venta'),
    path('eliminar/<int:ventaId>/', views.eliminar_venta_view, name='eliminar_venta'),
    path('estadisticas/', views.estadisticas_view, name='estadisticas_venta'),
]