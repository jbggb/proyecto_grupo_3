from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    
    # Productos
    path('productos/', views.productos, name='productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    
    # Clientes
    path('clientes/', views.clientes, name='clientes'),
    
    # Ventas
    path('ventas/', views.ventas, name='ventas'),
    
    # Administrador
    path('registro/', views.registrar_administrador, name='registro_administrador'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
]
