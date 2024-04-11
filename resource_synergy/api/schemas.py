from .models import Analysis, SynergyResult, Site, SiteAttribute
from ninja import ModelSchema, Schema


class SynergyResultSchema(ModelSchema):
    class Meta:
        model = SynergyResult
        fields = "__all__"


class SiteSchema(ModelSchema):
    class Meta:
        model = Site
        fields = "__all__"


class SiteCreateSchema(Schema):
    name: str
    description: str
    latitude: float
    longitude: float
    elevation: float
    resources_description: str


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


class AnalysisSitePatch(Schema):
    site_id: int


class ErrorSchema(Schema):
    detail: str
    code: str
    more_info: str | None = None
