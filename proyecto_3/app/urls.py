from django.urls import path
from app.views.Auth import views as auth_views
from app.views.Index import views as index_views
from app.views.Productos import views as productos_views
from app.views.Clientes import views as clientes_views
from app.views.Proveedores import views as proveedores_views
from app.views.Compras import views as compras_views
from app.views.Ventas import views as ventas_views
from app.views.Reportes import views as reportes_views
from app.views.Administradores import views as admin_views
from app.views.Marcas import views as marcas_views
from app.views.Tipo_producto import views as tipos_views
from app.views.Unidades import views as unidades_views

urlpatterns = [
    # Inicio
    path('', index_views.index, name='inicio'),

    # Auth
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('registro/', auth_views.registrar_administrador, name='registro_administrador'),

    # Productos
    path('productos/', productos_views.productos, name='productos'),
    path('productos/crear/', productos_views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', productos_views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', productos_views.eliminar_producto, name='eliminar_producto'),

    # Marcas
    path('marcas/', marcas_views.marcas, name='marcas'),
    path('marcas/crear/', marcas_views.crear_marca, name='crear_marca'),
    path('marcas/eliminar/<int:id>/', marcas_views.eliminar_marca, name='eliminar_marca'),

    # Tipos
    path('tipos/', tipos_views.tipos, name='tipos'),
    path('tipos/crear/', tipos_views.crear_tipo, name='crear_tipo'),
    path('tipos/eliminar/<int:id>/', tipos_views.eliminar_tipo, name='eliminar_tipo'),

    # Unidades
    path('unidades/', unidades_views.unidades, name='unidades'),
    path('unidades/crear/', unidades_views.crear_unidad, name='crear_unidad'),
    path('unidades/eliminar/<int:id>/', unidades_views.eliminar_unidad, name='eliminar_unidad'),

    # Clientes
    path('clientes/', clientes_views.clientes, name='clientes'),
    path('clientes/crear/', clientes_views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', clientes_views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', clientes_views.eliminar_cliente, name='eliminar_cliente'),

    # Ventas
    path('ventas/', ventas_views.ventas, name='ventas'),
    path('ventas/crear/', ventas_views.crear_venta, name='crear_venta'),
    path('ventas/detalle/<int:id>/', ventas_views.detalle_venta, name='detalle_venta'),
    path('ventas/editar/<int:id>/', ventas_views.editar_venta, name='editar_venta'),
    path('ventas/completar/<int:id>/', ventas_views.completar_venta, name='completar_venta'),
    path('ventas/eliminar/<int:id>/', ventas_views.eliminar_venta, name='eliminar_venta'),
    path('ventas/estadisticas/', ventas_views.estadisticas_ventas, name='estadisticas_ventas'),

    # Proveedores
    path('proveedores/', proveedores_views.proveedores, name='proveedores'),
    path('proveedores/crear/', proveedores_views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', proveedores_views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', proveedores_views.eliminar_proveedor, name='eliminar_proveedor'),

    # Compras
    path('compras/', compras_views.compras, name='compras'),
    path('compras/crear/', compras_views.crear_compra, name='crear_compra'),
    path('compras/editar/<int:id>/', compras_views.editar_compra, name='editar_compra'),
    path('compras/eliminar/<int:id>/', compras_views.eliminar_compra, name='eliminar_compra'),

    # Administrador
    path('admin/registro/', admin_views.admin_registro, name='admin_registro'),

    # Reportes
    path('reportes/', reportes_views.reportes, name='reportes'),
]