# Generated by Django 5.0.4 on 2024-04-10 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('analysis_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('site_id', models.IntegerField()),
                ('demand', models.FloatField()),
                ('seed_alternatives', models.CharField(max_length=255)),
                ('total_alternatives', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('criteria_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('dimension', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
                ('criteria_type', models.CharField(max_length=255)),
                ('criteria_unit', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CriteriaData',
            fields=[
                ('criteria_data_id', models.AutoField(primary_key=True, serialize=False)),
                ('criteria_id', models.IntegerField()),
                ('resource_id', models.IntegerField()),
                ('value', models.FloatField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('site_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('resource_type', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ResourceVariable',
            fields=[
                ('variable_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
                ('frequency', models.CharField(max_length=255)),
                ('date_added', models.DateTimeField()),
                ('date_updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('scenario_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('criteria_weight', models.JSONField()),
                ('subcriteria_weight', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('site_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('elevation', models.FloatField()),
                ('resources_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SiteAttribute',
            fields=[
                ('site_attribute_id', models.AutoField(primary_key=True, serialize=False)),
                ('site_id', models.IntegerField()),
                ('attribute_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('value', models.FloatField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SynergyResult',
            fields=[
                ('result_id', models.AutoField(primary_key=True, serialize=False)),
                ('analysis_id', models.IntegerField()),
                ('scenario_id', models.IntegerField()),
                ('total_installed_capacity', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSerie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable_id', models.IntegerField()),
                ('time_stamp', models.DateTimeField()),
                ('value', models.FloatField()),
            ],
        ),
    ]