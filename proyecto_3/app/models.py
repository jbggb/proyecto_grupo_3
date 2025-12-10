from django.db import models
from datetime import datetime
from decimal import Decimal

# Create your models here.

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
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    fechaRegistro = models.DateField(default=datetime.now)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        db_table = "cliente"


class Marca(models.Model):
    nombreMarca = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombreMarca
    
    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marcas"
        db_table = "marca"


class TipoProductos(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_tipo
    
    class Meta:
        verbose_name = "tipo_producto"
        verbose_name_plural = "tipos_productos"
        db_table = "tipo_productos"


class unidad_medida(models.Model):
    nombre_unidad = models.CharField(max_length=100)
    abreviatura = models.CharField(max_length=10)
    
    def __str__(self):
        return self.nombre_unidad
    
    class Meta:
        verbose_name = "unidad_medida"
        verbose_name_plural = "unidades_medida"
        db_table = "unidad_medida"


class Producto(models.Model):
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
    envio = models.IntegerField(default=1)
    fechaRegistro = models.DateField(default=datetime.now)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "proveedor"
        verbose_name_plural = "proveedores"
        db_table = "proveedor"


class Venta(models.Model):
    idAdministrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, db_column='idAdministrador')
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='idCliente')
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='idProducto')
    fechaVenta = models.DateField(default=datetime.now)
    totalVenta = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Venta {self.id}"
    
    class Meta:
        verbose_name = "venta"
        verbose_name_plural = "ventas"
        db_table = "venta"


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


class compra(models.Model):
    Administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    Proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    Producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_compra = models.DateField(default=datetime.now)
    totalcompra = models.FloatField()
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = "compra"


class Reporte(models.Model):
    idCompra = models.ForeignKey(compra, on_delete=models.CASCADE, db_column='idCompra', null=True, blank=True)
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