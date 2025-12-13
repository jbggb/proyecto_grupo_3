from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='inicio'),
    path('productos/', productos, name='productos'),
    path('clientes/', clientes, name='clientes'),
    path('ventas/', ventas, name='ventas'),
]
