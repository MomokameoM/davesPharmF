# Generated by Django 4.2.7 on 2023-12-06 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drug_store', '0018_saledetails_remission_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saledetails',
            name='remission_note',
            field=models.ForeignKey(db_column='remission_note_id', on_delete=django.db.models.deletion.CASCADE, to='drug_store.remissionnote', verbose_name='Nota de Remisión'),
        ),
    ]
