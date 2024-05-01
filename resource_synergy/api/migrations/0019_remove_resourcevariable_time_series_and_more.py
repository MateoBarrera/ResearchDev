# Generated by Django 5.0.4 on 2024-04-11 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_timeseries_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourcevariable',
            name='time_series',
        ),
        migrations.DeleteModel(
            name='TimeSeries',
        ),
        migrations.AddField(
            model_name='resourcevariable',
            name='time_series',
            field=models.JSONField(blank=True, null=True),
        ),
    ]