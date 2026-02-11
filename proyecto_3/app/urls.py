from django.urls import path
from . import views

urlpatterns = [
    # ===== PÁGINA DE INICIO =====
    path('', views.index, name='inicio'),
    
    # ===== PRODUCTOS =====
    path('productos/', views.productos, name='productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    
    # ===== CLIENTES =====
    path('clientes/', views.clientes, name='clientes'),
    
    # ===== VENTAS =====
    path('ventas/', views.ventas, name='ventas'),
    
    # ===== ADMINISTRADORES =====
    path('registro/', views.registrar_administrador, name='registro_administrador'),
]