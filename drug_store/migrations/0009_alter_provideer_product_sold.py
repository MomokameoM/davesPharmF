# Generated by Django 4.2.7 on 2023-12-06 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug_store', '0008_alter_provideer_product_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provideer',
            name='product_sold',
            field=models.CharField(max_length=100, verbose_name='Producto'),
        ),
    ]