# Generated by Django 3.2.12 on 2023-06-02 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamiento', '0007_alter_lugar_lugar'),
        ('usuarios', '0009_datosusuarios_centrocomercial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosusuarios',
            name='centroComercial',
            field=models.ForeignKey(blank=True, default=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='estacionamiento.centrocomercialespecifico'),
        ),
    ]