from django.db import models


class Analysis(models.Model):
    analysis_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    site_id = models.IntegerField()
    demand = models.FloatField()
    seed_alternatives = models.CharField(max_length=255)
    total_alternatives = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class SynergyResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    analysis_id = models.IntegerField()
    scenario_id = models.IntegerField()
    total_installed_capacity = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Scenario(models.Model):
    scenario_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    criteria_weight = models.JSONField()
    subcriteria_weight = models.JSONField()


class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField()
    resources_description = models.TextField()


class SiteAttribute(models.Model):
    site_attribute_id = models.AutoField(primary_key=True)
    site_id = models.IntegerField()
    attribute_id = models.IntegerField()
    name = models.CharField(max_length=255)
    value = models.FloatField()
    description = models.TextField()


class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    site_id = models.IntegerField()
    name = models.CharField(max_length=255)
    resource_type = models.CharField(
        max_length=255
    )  # Asumiendo que "ResourceType" es una cadena
    description = models.TextField()


class ResourceVariable(models.Model):
    variable_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)  # Asumiendo que "Unit" es una cadena
    source = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)
    date_added = models.DateTimeField()
    date_updated = models.DateTimeField()


class TimeSerie(models.Model):
    variable_id = models.IntegerField()
    time_stamp = models.DateTimeField()
    value = models.FloatField()


class Criteria(models.Model):
    criteria_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    dimension = models.CharField(
        max_length=255
    )  # Asumiendo que "Dimension" es una cadena
    source = models.CharField(max_length=255)
    criteria_type = models.CharField(
        max_length=255
    )  # Asumiendo que "CriteriaType" es una cadena
    criteria_unit = models.CharField(
        max_length=255
    )  # Asumiendo que "Unit" es una cadena


class CriteriaData(models.Model):
    criteria_data_id = models.AutoField(primary_key=True)
    criteria_id = models.IntegerField()
    resource_id = models.IntegerField()
    value = models.FloatField()
    date = models.DateTimeField()
