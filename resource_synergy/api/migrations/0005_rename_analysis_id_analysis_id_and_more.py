# Generated by Django 5.0.4 on 2024-04-11 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_analysis_site_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='analysis',
            old_name='analysis_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='analysis',
            old_name='site_id',
            new_name='site',
        ),
        migrations.RenameField(
            model_name='site',
            old_name='site_id',
            new_name='id',
        ),
    ]