# Generated by Django 5.0.4 on 2024-04-11 18:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_resourcevariable_frequency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('resource_type', models.CharField(choices=[('Hydro', 'Hydro'), ('Solar', 'Solar'), ('Wind', 'Wind'), ('Biomass', 'Biomass')], max_length=25)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='resource',
            name='resource_variables',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='site',
        ),
        migrations.DeleteModel(
            name='SiteAttribute',
        ),
        migrations.RemoveField(
            model_name='site',
            name='resources_description',
        ),
        migrations.AddField(
            model_name='site',
            name='resources',
            field=models.ManyToManyField(related_name='variable', to='api.resourcevariable'),
        ),
        migrations.AddField(
            model_name='source',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.site'),
        ),
        migrations.DeleteModel(
            name='Resource',
        ),
    ]
