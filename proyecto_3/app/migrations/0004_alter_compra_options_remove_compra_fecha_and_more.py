import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_cliente_documento_alter_cliente_telefono'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compra',
            options={'ordering': ['-fechaCompra'], 'verbose_name': 'compra', 'verbose_name_plural': 'compras'},
        ),
        migrations.AlterField(
            model_name='administrador',
            name='idAdministrador',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='documento',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='compra',
            name='estado',
            field=models.CharField(default='Pendiente', max_length=50),
        ),
        migrations.AlterField(
            model_name='compra',
            name='idCompra',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='cantidad',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
    ]