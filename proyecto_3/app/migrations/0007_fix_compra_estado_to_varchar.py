from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_administrador_idadministrador_and_more'),
    ]

    operations = [
        # 1. Primero convertir los valores 0/1 existentes a texto
        migrations.RunSQL(
            sql="""
                ALTER TABLE compra MODIFY estado VARCHAR(50) NOT NULL DEFAULT 'Pendiente';
                UPDATE compra SET estado = 'Pendiente'  WHERE estado = '0';
                UPDATE compra SET estado = 'Completada' WHERE estado = '1';
            """,
            reverse_sql="""
                UPDATE compra SET estado = '0' WHERE estado = 'Pendiente';
                UPDATE compra SET estado = '1' WHERE estado = 'Completada';
                ALTER TABLE compra MODIFY estado TINYINT(1) NOT NULL DEFAULT 0;
            """,
        ),
        # 2. Decirle a Django que ahora el campo tiene choices
        migrations.AlterField(
            model_name='compra',
            name='estado',
            field=models.CharField(
                choices=[('Pendiente', 'Pendiente'), ('Completada', 'Completada')],
                default='Pendiente',
                max_length=50,
            ),
        ),
    ]