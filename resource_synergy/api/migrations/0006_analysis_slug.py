# Generated by Django 5.0.4 on 2024-04-11 06:26

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_analysis_id_analysis_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True),
        ),
    ]
