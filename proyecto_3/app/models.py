from django.db import models
from datetime import datetime
from decimal import Decimal


class Administrador(models.Model):
    nombre = models.CharField(max_length=150)
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    fechaRegistro = models.DateField(default=datetime.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "administrador"
        verbose_name_plural = "administradores"
        db_table = "administrador"


class Cliente(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    nombre = models.CharField(max_length=150)
    documento = models.CharField(max_length=12, blank=True, default='', db_column='documento')
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, default='')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fechaRegistro = models.DateField(default=datetime.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        db_table = "cliente"


class Marca(models.Model):
    idMarca = models.AutoField(primary_key=True, db_column='idMarca')
    nombreMarca = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreMarca

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marcas"
        db_table = "marca"


class TipoProductos(models.Model):
    idTipo = models.AutoField(primary_key=True, db_column='idTipo')
    nombre_tipo = models.CharField(max_length=100, db_column='nombre')
    descripcion = models.TextField(db_column='descripcion', blank=True, default='')

    def __str__(self):
        return self.nombre_tipo

    class Meta:
        verbose_name = "tipo_producto"
        verbose_name_plural = "tipos_productos"
        db_table = "tipoproducto"


class unidad_medida(models.Model):
    idUnidad = models.AutoField(primary_key=True, db_column='idUnidad')
    nombre_unidad = models.CharField(max_length=100, db_column='nombreUnidad')
    abreviatura = models.CharField(max_length=10, db_column='abreviatura', blank=True, default='-')

    def __str__(self):
        return self.nombre_unidad

    class Meta:
        verbose_name = "unidad_medida"
        verbose_name_plural = "unidades_medida"
        db_table = "unidadmedida"


class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True, db_column='idProducto')
    idTipo = models.ForeignKey(TipoProductos, on_delete=models.CASCADE, db_column='idTipo')
    idMarca = models.ForeignKey(Marca, on_delete=models.CASCADE, db_column='idMarca')
    idUnidad = models.ForeignKey(unidad_medida, on_delete=models.CASCADE, db_column='idUnidad')
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        db_table = "producto"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    envio = models.IntegerField(default=0)
    fechaRegistro = models.DateField(default=datetime.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"
        db_table = "proveedor"


# ===== MODELO DE VENTAS (Ricardo) =====
class Venta(models.Model):
    ESTADO_CHOICES = [
        ('Completada', 'Completada'),
        ('Pendiente', 'Pendiente'),
    ]
    cliente = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente}"

    class Meta:
        verbose_name = "venta"
        verbose_name_plural = "ventas"
        db_table = "venta"
        ordering = ['-fecha']


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto_nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(default=1)

    @property
    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"{self.producto_nombre} x{self.cantidad}"

    class Meta:
        db_table = "detalle_venta"


# ===== MODELO DE COMPRAS (MOJICA) =====
class Compra(models.Model):
    fecha = models.DateField(default=datetime.now)
    estado = models.BooleanField(default=False)
    Administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, db_column='Administrador_id')
    Producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='Producto_id')
    Proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, db_column='Proveedor_id')

    def __str__(self):
        return f"Compra #{self.id}"

    class Meta:
        db_table = "compra"
        verbose_name = "compra"
        verbose_name_plural = "compras"
        ordering = ['-fecha']


class Pedidos(models.Model):
    id_administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateField()
    estado_pedido = models.CharField(max_length=150)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido {self.id}"

    class Meta:
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"
        db_table = "pedidos"
        ordering = ['-fecha_pedido']


class Reporte(models.Model):
    idCompra = models.ForeignKey(Compra, on_delete=models.CASCADE, db_column='idCompra', null=True, blank=True)
    idPedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, db_column='idPedido', null=True, blank=True)
    idVenta = models.ForeignKey(Venta, on_delete=models.CASCADE, db_column='idVenta', null=True, blank=True)
    idAdministrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, db_column='idAdministrador')
    fechaReporte = models.DateTimeField()
    descripcion = models.TextField()

    def __str__(self):
        return f"Reporte {self.id}"

    class Meta:
        verbose_name = "reporte"
        verbose_name_plural = "reportes"
        db_table = "reporte"