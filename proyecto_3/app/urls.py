from django.urls import path
from app import views

urlpatterns = [
    # Inicio
    path('', views.index, name='inicio'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registrar_administrador, name='registro_administrador'),

    # Productos
    path('productos/', views.productos, name='productos'),
    path('productos/json/', views.productos_json, name='productos_json'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # Marcas
    path('marcas/crear/', views.crear_marca, name='crear_marca'),
    path('marcas/eliminar/<int:id>/', views.eliminar_marca, name='eliminar_marca'),

    # Tipos
    path('tipos/crear/', views.crear_tipo, name='crear_tipo'),
    path('tipos/eliminar/<int:id>/', views.eliminar_tipo, name='eliminar_tipo'),

    # Unidades
    path('unidades/crear/', views.crear_unidad, name='crear_unidad'),
    path('unidades/eliminar/<int:id>/', views.eliminar_unidad, name='eliminar_unidad'),

    # Clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/json/', views.clientes_json, name='clientes_json'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    # Ventas
    path('ventas/', views.ventas, name='ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),
    path('ventas/detalle/<int:id>/', views.detalle_venta, name='detalle_venta'),
    path('ventas/editar/<int:id>/', views.editar_venta, name='editar_venta'),
    path('ventas/completar/<int:id>/', views.completar_venta, name='completar_venta'),
    path('ventas/eliminar/<int:id>/', views.eliminar_venta, name='eliminar_venta'),
    path('ventas/estadisticas/', views.estadisticas_ventas, name='estadisticas_ventas'),

    # Proveedores
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/json/', views.proveedores_json, name='proveedores_json'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    # Compras
    path('compras/', views.compras, name='compras'),
    path('compras/json/', views.compras_json, name='compras_json'),
    path('compras/crear/', views.crear_compra, name='crear_compra'),
    path('compras/editar/<int:id>/', views.editar_compra, name='editar_compra'),
    path('compras/eliminar/<int:id>/', views.eliminar_compra, name='eliminar_compra'),

    # Administrador
    path('admin/productos/', views.admin_productos, name='admin_productos'),
    path('admin/registro/', views.admin_registro, name='admin_registro'),

    # Reportes
    path('reportes/', views.reportes, name='reportes'),
]
