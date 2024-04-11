from .models import Analysis, SynergyResult, Site, SiteAttribute
from ninja import ModelSchema, Schema


class SiteSchema(ModelSchema):
    class Meta:
        model = Site
        fields = "__all__"


class AnalysisSchema(ModelSchema):
    site: SiteSchema | None = None

    class Meta:
        model = Analysis
        fields = "__all__"


class AnalysisCreateSchema(Schema):
    name: str
    description: str
    site_id: int | None = None
    demand: float
    seed_alternatives: str
    total_alternatives: int


class SynergyResultSchema(ModelSchema):
    class Meta:
        model = SynergyResult
        fields = "__all__"


class SiteAttributeSchema(ModelSchema):
    class Meta:
        model = SiteAttribute
        fields = "__all__"


class ErrorSchema(Schema):
    detail: str
    code: str
    more_info: str | None = None


class AnalysisSitePatch(Schema):
    site_id: int
