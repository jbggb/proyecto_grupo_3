# Generated migration to add FK from DetalleVenta to Producto

import django.db.models.deletion
from django.db import migrations, models


def forward_populate_producto_fk(apps, schema_editor):
    """
    Puebla el campo producto_id en DetalleVenta basado en producto_nombre.
    Si hay múltiples productos con el mismo nombre, usa el primero encontrado.
    """
    DetalleVenta = apps.get_model('app', 'DetalleVenta')
    Producto = apps.get_model('app', 'Producto')

    updated = 0
    failed = 0

    for detalle in DetalleVenta.objects.all():
        try:
            # Buscar por nombre exacto
            producto = Producto.objects.filter(nombre=detalle.producto_nombre).first()
            if producto:
                detalle.producto = producto
                detalle.save()
                updated += 1
            else:
                failed += 1
        except Exception as e:
            print(f"Error procesando detalle {detalle.id}: {str(e)}")
            failed += 1

    print(f"\nMigración DetalleVenta.producto: {updated} actualizado(s), {failed} fallido(s)")


def reverse_clear_producto_fk(apps, schema_editor):
    """
    Reversa: limpiar el campo producto_id (NO eliminar, por compatibilidad)
    """
    DetalleVenta = apps.get_model('app', 'DetalleVenta')
    DetalleVenta.objects.all().update(producto=None)


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        # 1. Agregar nuevo campo producto (FK nullable)
        migrations.AddField(
            model_name='detalleventa',
            name='producto',
            field=models.ForeignKey(blank=True, db_column='producto_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.producto'),
        ),

        # 2. Migración de datos: poblar FK basado en producto_nombre
        migrations.RunPython(
            forward_populate_producto_fk,
            reverse_clear_producto_fk
        ),
    ]
