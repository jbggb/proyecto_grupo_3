from django.urls import path, include  # ← CAMBIO AQUÍ
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
    
    # Ventas(Ricardo)
    path('ventas/', include('ventas.urls')),  # ← CAMBIO AQUÍ
    
    # Registro
    path('registro/', views.registrar_administrador, name='registro_administrador'),
    
    # Login y logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Proveedores
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    # Administrador (diego)
    path('admin/productos/', views.admin_productos, name='admin_productos'),
    path('admin/registro/', views.admin_registro, name='admin_registro'),
    path('reportes/', views.reportes, name='reportes'),
    
    # Compras (MOJICA)
    path('compras/', views.compras, name='compras'),
]