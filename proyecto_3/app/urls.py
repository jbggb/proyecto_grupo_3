from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('productos/', views.productos, name='productos'),
    path('clientes/', views.clientes, name='clientes'),
    path('ventas/', views.ventas, name='ventas'),
    path('registro/', views.registrar_administrador, name='registro_administrador'),
    path('compras/', views.comprasCreateview.as_view(), name='compras'),
    path('compras/<int:pk>/eliminar/', views.ComprasDeleteView.as_view(), name='compras_eliminar')
]