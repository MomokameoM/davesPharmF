# Generated by Django 4.2.7 on 2023-12-06 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drug_store', '0005_remissionnote_remove_product_payment_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'verbose_name_plural': 'Factura'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name_plural': 'Clientes'},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name_plural': 'Empleados'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterModelOptions(
            name='provideer',
            options={'verbose_name_plural': 'Proveedores'},
        ),
        migrations.AlterModelOptions(
            name='remissionnote',
            options={'verbose_name_plural': 'Notas de Remision'},
        ),
        migrations.AlterModelOptions(
            name='saledetails',
            options={'verbose_name_plural': 'Detalles de ventas'},
        ),
    ]
