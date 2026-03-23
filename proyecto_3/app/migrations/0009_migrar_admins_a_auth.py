from django.db import migrations
from django.contrib.auth.hashers import make_password


def migrar_admins(apps, schema_editor):
    Administrador = apps.get_model('app', 'Administrador')
    User = apps.get_model('auth', 'User')

    for admin in Administrador.objects.all():
        if not User.objects.filter(username=admin.usuario).exists():
            User.objects.create(
                username=admin.usuario,
                password=make_password('Fabian1234'),
                email=admin.email if admin.email else '',
                is_active=True,
                is_superuser=True,
                is_staff=True,
            )


def revertir(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_compra_cantidad_precio'),
    ]

    operations = [
        migrations.RunPython(migrar_admins, revertir),
    ]