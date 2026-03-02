# Importaciones centralizadas de todas las vistas del sistema
from .Index.views import index
from .Auth.views import login_view, logout_view, registrar_administrador
from .Productos.views import (
    productos, crear_producto, editar_producto, eliminar_producto,
    admin_productos, productos_json
)
from .Marcas.views import crear_marca, eliminar_marca
from .Tipos.views import crear_tipo, eliminar_tipo
from .Unidades.views import crear_unidad, eliminar_unidad
from .Clientes.views import clientes, crear_cliente, editar_cliente, eliminar_cliente, clientes_json
from .Ventas.views import (
    ventas, crear_venta, detalle_venta, editar_venta,
    completar_venta, eliminar_venta, estadisticas_ventas
)
from .Proveedores.views import (
    proveedores, crear_proveedor, editar_proveedor, eliminar_proveedor, proveedores_json
)
from .Compras.views import (
    compras, crear_compra, editar_compra, eliminar_compra, compras_json
)
from .Administradores.views import admin_registro
from .Reportes.views import reportes

__all__ = [
    # Index
    'index',
    # Auth
    'login_view', 'logout_view', 'registrar_administrador',
    # Productos
    'productos', 'crear_producto', 'editar_producto', 'eliminar_producto',
    'admin_productos', 'productos_json',
    # Marcas
    'crear_marca', 'eliminar_marca',
    # Tipos
    'crear_tipo', 'eliminar_tipo',
    # Unidades
    'crear_unidad', 'eliminar_unidad',
    # Clientes
    'clientes', 'crear_cliente', 'editar_cliente', 'eliminar_cliente', 'clientes_json',
    # Ventas
    'ventas', 'crear_venta', 'detalle_venta', 'editar_venta',
    'completar_venta', 'eliminar_venta', 'estadisticas_ventas',
    # Proveedores
    'proveedores', 'crear_proveedor', 'editar_proveedor', 'eliminar_proveedor', 'proveedores_json',
    # Compras
    'compras', 'crear_compra', 'editar_compra', 'eliminar_compra', 'compras_json',
    # Administradores
    'admin_registro',
    # Reportes
    'reportes',
]
