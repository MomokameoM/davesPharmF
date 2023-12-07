# Generated by Django 4.2.7 on 2023-12-06 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drug_store', '0007_alter_remissionnote_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provideer',
            name='product_sold',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drug_store.product', verbose_name='Producto Vendido'),
        ),
    ]
