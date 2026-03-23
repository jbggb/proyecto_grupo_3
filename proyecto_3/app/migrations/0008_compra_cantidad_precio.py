from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_fix_compra_estado_to_varchar'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='compra',
            name='precio_unitario',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]