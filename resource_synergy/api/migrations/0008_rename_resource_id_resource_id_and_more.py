# Generated by Django 5.0.4 on 2024-04-11 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_analysis_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='resource_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='site_id',
        ),
        migrations.AddField(
            model_name='resource',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.site'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource_type',
            field=models.CharField(choices=[('Hydro', 'Hydro'), ('Solar', 'Solar'), ('Wind', 'Wind'), ('Biomass', 'Biomass')], max_length=25),
        ),
        migrations.AlterField(
            model_name='resourcevariable',
            name='unit',
            field=models.CharField(choices=[('m/s', 'METER_PER_SECOND'), ('m³', 'CUBIT_METER'), ('Celsius', 'CELSIUS'), ('Fahrenheit', 'FAHRENHEIT')], max_length=20),
        ),
    ]