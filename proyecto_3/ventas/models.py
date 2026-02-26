from django.db import models

class venta(models.Model):
    cliente = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('completada', 'Completada'),
        ('pendiente', 'Pendiente'),
        ('cancelada', 'Cancelada'),
    ], default='completada')

class detalle_venta(models.Model):
    venta = models.ForeignKey(venta, on_delete=models.CASCADE)
    producto_nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)