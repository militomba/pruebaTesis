# Generated by Django 3.2.12 on 2023-06-02 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estacionamiento', '0007_alter_lugar_lugar'),
        ('usuarios', '0003_auto_20230602_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosusuarios',
            name='centroComercial',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='centroComercial', to='estacionamiento.centrocomercialespecifico'),
        ),
    ]