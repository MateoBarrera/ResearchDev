# Generated by Django 5.0.4 on 2024-04-11 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_rename_timeserie_timeseries_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeseries',
            name='id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
