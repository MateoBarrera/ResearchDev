from .models import Analysis, SynergyResult, Site, SiteAttribute
from ninja import ModelSchema


class AnalysisSchema(ModelSchema):
    class Meta:
        model = Analysis
        fields = "__all__"


class AnalysisSchemaIn(ModelSchema):
    class Meta:
        model = Analysis
        exclude = ["analysis_id", "date_created", "date_updated"]


class SynergyResultSchema(ModelSchema):
    class Meta:
        model = SynergyResult
        fields = "__all__"


class SiteSchema(ModelSchema):
    class Meta:
        model = Site
        fields = "__all__"


class SiteAttributeSchema(ModelSchema):
    class Meta:
        model = SiteAttribute
        fields = "__all__"
