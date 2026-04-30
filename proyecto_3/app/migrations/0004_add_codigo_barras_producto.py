from django.db import migrations, models


class Migration(migrations.Migration):

    # Cambia este nombre por el de tu última migración en app/migrations/
    # Puedes verlo con: python manage.py showmigrations app
    dependencies = [
        ('app', '0003_notificacionemail_delete_administrador'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='codigo_barras',
            field=models.CharField(
                max_length=50,
                blank=True,
                default='',
                db_index=True,
                verbose_name='Código de barras',
            ),
        ),
    ]
