"""
Migración 0011: Cambia la FK de Compra.Administrador (tabla propia)
a django.contrib.auth.User.

RAZÓN: La tabla 'administrador' estaba vacía porque el sistema migró
su autenticación a Django nativo. Cualquier intento de crear una compra
fallaba con "Tu usuario no tiene un administrador asociado".

ESTRATEGIA:
- Se agrega el campo 'usuario' (FK a auth.User, nullable temporalmente).
- Se elimina el campo 'Administrador' (FK a la tabla propia).
- La lógica de ComprasView ya usa request.user directamente.
"""
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_compra_producto_alter_detalleventa_cantidad'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 1. Agregar nueva columna usuario_id apuntando a auth_user (nullable primero)
        migrations.AddField(
            model_name='compra',
            name='usuario',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                db_column='usuario_id',
                related_name='compras',
                verbose_name='Usuario',
            ),
        ),
        # 2. Eliminar la vieja FK a la tabla administrador propia
        migrations.RemoveField(
            model_name='compra',
            name='Administrador',
        ),
    ]
