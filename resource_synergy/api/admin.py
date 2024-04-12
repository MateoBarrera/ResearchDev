from django.contrib import admin
from api.models import (
    Site,
    Analysis,
    SynergyResult,
    Scenario,
    Source,
    ResourceVariable,
)

# Register your models here.
admin.site.register(Site)
admin.site.register(Analysis)
admin.site.register(SynergyResult)
admin.site.register(Scenario)
admin.site.register(Source)
admin.site.register(ResourceVariable)
