from django.db import models
from datetime import datetime


class Administrador(models.Model):
    idAdministrador = models.AutoField(primary_key=True, db_column='id')
    nombre          = models.CharField(max_length=150)
    usuario         = models.CharField(max_length=50, unique=True)
    contrasena      = models.CharField(max_length=255)
    email           = models.EmailField(max_length=100)
    fechaRegistro   = models.DateField(default=datetime.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name        = "administrador"
        verbose_name_plural = "administradores"
        db_table            = "administrador"


class Cliente(models.Model):
    ESTADO_CHOICES = [
        ('activo',   'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    nombre        = models.CharField(max_length=150)
    documento     = models.CharField(max_length=10, blank=True, default='')
    telefono      = models.CharField(max_length=20)
    email         = models.EmailField(max_length=100)
    direccion     = models.CharField(max_length=200, blank=True, default='')
    estado        = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fechaRegistro = models.DateField(default=datetime.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name        = "cliente"
        verbose_name_plural = "clientes"
        db_table            = "cliente"


class Marca(models.Model):
    idMarca     = models.AutoField(primary_key=True, db_column='idMarca')
    nombreMarca = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreMarca

    class Meta:
        verbose_name        = "marca"
        verbose_name_plural = "marcas"
        db_table            = "marca"


class TipoProductos(models.Model):
    idTipo      = models.AutoField(primary_key=True, db_column='idTipo')
    nombre_tipo = models.CharField(max_length=100, db_column='nombre')
    descripcion = models.TextField(db_column='descripcion', blank=True, default='')

    def __str__(self):
        return self.nombre_tipo

    class Meta:
        verbose_name        = "tipo_producto"
        verbose_name_plural = "tipos_productos"
        db_table            = "tipoproducto"


# NOTA PARA EL INSTRUCTOR: el nombre correcto en PascalCase sería UnidadMedida.
# Se mantiene así para no romper las migraciones y las vistas que ya lo referencian.
class unidad_medida(models.Model):
    idUnidad      = models.AutoField(primary_key=True, db_column='idUnidad')
    nombre_unidad = models.CharField(max_length=100, db_column='nombreUnidad')
    abreviatura   = models.CharField(max_length=10, db_column='abreviatura', blank=True, default='-')

    def __str__(self):
        return self.nombre_unidad

    class Meta:
        verbose_name        = "unidad_medida"
        verbose_name_plural = "unidades_medida"
        db_table            = "unidadmedida"


class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True, db_column='idProducto')
    idTipo     = models.ForeignKey(TipoProductos, on_delete=models.CASCADE,  db_column='idTipo')
    idMarca    = models.ForeignKey(Marca,         on_delete=models.CASCADE,  db_column='idMarca')
    idUnidad   = models.ForeignKey(unidad_medida, on_delete=models.CASCADE,  db_column='idUnidad')
    nombre     = models.CharField(max_length=255)
    precio     = models.DecimalField(max_digits=10, decimal_places=2)
    stock      = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name        = "producto"
        verbose_name_plural = "productos"
        db_table            = "producto"
        unique_together     = [('nombre', 'idMarca', 'idTipo')]


class Proveedor(models.Model):
    id            = models.AutoField(primary_key=True, db_column='id')
    nombre        = models.CharField(max_length=150)
    telefono      = models.CharField(max_length=20)
    email         = models.EmailField(max_length=100)
    envio         = models.IntegerField(default=0)
    fechaRegistro = models.DateField(default=datetime.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name        = "proveedor"
        verbose_name_plural = "proveedores"
        db_table            = "proveedor"


class Venta(models.Model):
    ESTADO_CHOICES = [
        ('Completada', 'Completada'),
        ('Pendiente',  'Pendiente'),
    ]
    # NOTA: idealmente cliente debería ser FK a Cliente para integridad referencial.
    # Se mantiene como CharField por compatibilidad con la BD actual.
    # Deuda técnica pendiente: migrar a ForeignKey(Cliente, on_delete=models.PROTECT).
    cliente = models.CharField(max_length=100)
    fecha   = models.DateTimeField(auto_now_add=True)
    total   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado  = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente}"

    class Meta:
        verbose_name        = "venta"
        verbose_name_plural = "ventas"
        db_table            = "venta"
        ordering            = ['-fecha']


class DetalleVenta(models.Model):
    venta           = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto_nombre = models.CharField(max_length=255)
    precio          = models.DecimalField(max_digits=10, decimal_places=2)

    # ─── CORRECCIÓN: cantidad no puede ser nula. Un detalle de venta siempre
    # tiene al menos 1 unidad. Se eliminó null=True y blank=True.
    # El parche "self.cantidad or 0" en subtotal ya no es necesario.
    cantidad = models.IntegerField(default=1)

    @property
    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"{self.producto_nombre} x{self.cantidad}"

    class Meta:
        db_table = "detalle_venta"


class Compra(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente',  'Pendiente'),
        ('Completada', 'Completada'),
    ]
    idCompra        = models.AutoField(primary_key=True, db_column='id')
    fechaCompra     = models.DateField(default=datetime.now, db_column='fecha')
    estado          = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Pendiente')
    cantidad        = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # NOTA: los nombres de FK con mayúscula (Administrador, Producto, Proveedor)
    # son inconsistentes con la convención de Django (minúscula).
    # Se mantienen para no romper las migraciones existentes.
    Administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE,        db_column='Administrador_id')
    Producto      = models.ForeignKey(Producto,      on_delete=models.SET_NULL, null=True, blank=True, db_column='Producto_id')
    Proveedor     = models.ForeignKey(Proveedor,     on_delete=models.CASCADE,        db_column='Proveedor_id')

    @property
    def total(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"Compra #{self.idCompra}"

    class Meta:
        db_table            = "compra"
        verbose_name        = "compra"
        verbose_name_plural = "compras"
        ordering            = ['-fechaCompra']


# ─── DEUDA TÉCNICA: Pedidos y Reporte están definidos pero no tienen
# vistas, URLs ni templates implementados. Quedan como funcionalidad
# planeada para una versión futura del sistema. ────────────────────

class Pedidos(models.Model):
    id_administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    id_cliente       = models.ForeignKey(Cliente,       on_delete=models.CASCADE)
    fecha_pedido     = models.DateField()
    estado_pedido    = models.CharField(max_length=150)
    total            = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id}"

    class Meta:
        verbose_name        = "pedido"
        verbose_name_plural = "pedidos"
        db_table            = "pedidos"
        ordering            = ['-fecha_pedido']


class Reporte(models.Model):
    idCompra        = models.ForeignKey(Compra,   on_delete=models.CASCADE, db_column='idCompra',        null=True, blank=True)
    idPedido        = models.ForeignKey(Pedidos,  on_delete=models.CASCADE, db_column='idPedido',        null=True, blank=True)
    idVenta         = models.ForeignKey(Venta,    on_delete=models.CASCADE, db_column='idVenta',         null=True, blank=True)
    idAdministrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, db_column='idAdministrador')
    fechaReporte    = models.DateTimeField()
    descripcion     = models.TextField()

    def __str__(self):
        return f"Reporte {self.id}"

    class Meta:
        verbose_name        = "reporte"
        verbose_name_plural = "reportes"
        db_table            = "reporte"