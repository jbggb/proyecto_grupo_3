import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('usuario', models.CharField(max_length=50, unique=True)),
                ('contrasena', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=100)),
                ('fechaRegistro', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'administrador',
                'verbose_name_plural': 'administradores',
                'db_table': 'administrador',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('documento', models.CharField(blank=True, db_column='documento', default='', max_length=12)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('direccion', models.CharField(blank=True, default='', max_length=200)),
                ('estado', models.CharField(
                    choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')],
                    default='activo', max_length=10)),
                ('fechaRegistro', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('idMarca', models.AutoField(db_column='idMarca', primary_key=True, serialize=False)),
                ('nombreMarca', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'marca',
                'verbose_name_plural': 'marcas',
                'db_table': 'marca',
            },
        ),
        migrations.CreateModel(
            name='TipoProductos',
            fields=[
                ('idTipo', models.AutoField(db_column='idTipo', primary_key=True, serialize=False)),
                ('nombre_tipo', models.CharField(db_column='nombre', max_length=100)),
                ('descripcion', models.TextField(blank=True, db_column='descripcion', default='')),
            ],
            options={
                'verbose_name': 'tipo_producto',
                'verbose_name_plural': 'tipos_productos',
                'db_table': 'tipoproducto',
            },
        ),
        migrations.CreateModel(
            name='unidad_medida',
            fields=[
                ('idUnidad', models.AutoField(db_column='idUnidad', primary_key=True, serialize=False)),
                ('nombre_unidad', models.CharField(db_column='nombreUnidad', max_length=100)),
                ('abreviatura', models.CharField(blank=True, db_column='abreviatura', default='-', max_length=10)),
            ],
            options={
                'verbose_name': 'unidad_medida',
                'verbose_name_plural': 'unidades_medida',
                'db_table': 'unidadmedida',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idProducto', models.AutoField(db_column='idProducto', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=0)),
                ('idMarca', models.ForeignKey(db_column='idMarca', on_delete=django.db.models.deletion.CASCADE, to='app.marca')),
                ('idTipo', models.ForeignKey(db_column='idTipo', on_delete=django.db.models.deletion.CASCADE, to='app.tipoproductos')),
                ('idUnidad', models.ForeignKey(db_column='idUnidad', on_delete=django.db.models.deletion.CASCADE, to='app.unidad_medida')),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
                'db_table': 'producto',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('envio', models.IntegerField(default=0)),
                ('fechaRegistro', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'proveedor',
                'verbose_name_plural': 'proveedores',
                'db_table': 'proveedor',
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('estado', models.CharField(
                    choices=[('Completada', 'Completada'), ('Pendiente', 'Pendiente')],
                    default='Pendiente', max_length=20)),
            ],
            options={
                'verbose_name': 'venta',
                'verbose_name_plural': 'ventas',
                'db_table': 'venta',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto_nombre', models.CharField(max_length=255)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad', models.IntegerField(default=1)),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='app.venta')),
            ],
            options={
                'db_table': 'detalle_venta',
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.datetime.now)),
                ('estado', models.BooleanField(default=False)),
                ('Administrador', models.ForeignKey(
                    db_column='Administrador_id',
                    on_delete=django.db.models.deletion.CASCADE,
                    to='app.administrador')),
                ('Producto', models.ForeignKey(
                    db_column='Producto_id',
                    on_delete=django.db.models.deletion.CASCADE,
                    to='app.producto')),
                ('Proveedor', models.ForeignKey(
                    db_column='Proveedor_id',
                    on_delete=django.db.models.deletion.CASCADE,
                    to='app.proveedor')),
            ],
            options={
                'verbose_name': 'compra',
                'verbose_name_plural': 'compras',
                'db_table': 'compra',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateField()),
                ('estado_pedido', models.CharField(max_length=150)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.administrador')),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cliente')),
            ],
            options={
                'verbose_name': 'pedido',
                'verbose_name_plural': 'pedidos',
                'db_table': 'pedidos',
                'ordering': ['-fecha_pedido'],
            },
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaReporte', models.DateTimeField()),
                ('descripcion', models.TextField()),
                ('idAdministrador', models.ForeignKey(
                    db_column='idAdministrador',
                    on_delete=django.db.models.deletion.CASCADE,
                    to='app.administrador')),
                ('idCompra', models.ForeignKey(
                    blank=True, db_column='idCompra', null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to='app.compra')),
                ('idPedido', models.ForeignKey(
                    blank=True, db_column='idPedido', null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to='app.pedidos')),
                ('idVenta', models.ForeignKey(
                    blank=True, db_column='idVenta', null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to='app.venta')),
            ],
            options={
                'verbose_name': 'reporte',
                'verbose_name_plural': 'reportes',
                'db_table': 'reporte',
            },
        ),
    ]
