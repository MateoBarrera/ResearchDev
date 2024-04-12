from uuid import uuid4
from django.db import models
from django_extensions.db.fields import AutoSlugField  # type: ignore
from api.enums import ResourceType, Unit, Frequency


class ResourceVariable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(
        max_length=20, choices=[(unit.value, unit.name) for unit in Unit]
    )  # Asumiendo que "Unit" es una cadena
    source = models.CharField(max_length=255)
    frequency = models.CharField(
        max_length=20,
        choices=[(frequency.value, frequency.name) for frequency in Frequency],
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    time_series = models.JSONField(null=True, blank=True)


class Site(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    resources = models.ManyToManyField(
        "ResourceVariable", related_name="variable", blank=True
    )

    def __str__(self):
        return self.name


class Analysis(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name")
    description = models.TextField()
    demand = models.FloatField()
    seed_alternatives = models.CharField(max_length=255)
    total_alternatives = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.id}"


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


class Source(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    resource_type = models.CharField(
        max_length=25,
        choices=[(resource.value, resource.name) for resource in ResourceType],
    )
    description = models.TextField()
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.id}"


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
