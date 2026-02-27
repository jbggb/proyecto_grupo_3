from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # AJAX Marca
    path('ajax/crear-marca/', views.crear_marca_ajax, name='crear_marca_ajax'),
    path('ajax/eliminar-marca/<int:id>/', views.eliminar_marca_ajax, name='eliminar_marca_ajax'),
    path('ajax/listar-marcas/', views.listar_marcas_ajax, name='listar_marcas_ajax'),

    # AJAX Tipo
    path('ajax/crear-tipo/', views.crear_tipo_ajax, name='crear_tipo_ajax'),
    path('ajax/eliminar-tipo/<int:id>/', views.eliminar_tipo_ajax, name='eliminar_tipo_ajax'),
    path('ajax/listar-tipos/', views.listar_tipos_ajax, name='listar_tipos_ajax'),

    # AJAX Unidad
    path('ajax/crear-unidad/', views.crear_unidad_ajax, name='crear_unidad_ajax'),
    path('ajax/eliminar-unidad/<int:id>/', views.eliminar_unidad_ajax, name='eliminar_unidad_ajax'),
    path('ajax/listar-unidades/', views.listar_unidades_ajax, name='listar_unidades_ajax'),

    path('clientes/', views.clientes, name='clientes'),
    path('ventas/', views.ventas, name='ventas'),
    path('registro/', views.registrar_administrador, name='registro_administrador'),
    path('reportes/', views.reportes, name='reportes'),
]