# Generated by Django 4.2.7 on 2023-12-06 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drug_store', '0019_alter_saledetails_remission_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saledetails',
            name='remission_note',
        ),
    ]