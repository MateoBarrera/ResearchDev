from importlib import resources
from .models import Analysis, SynergyResult, Site, ResourceVariable, Source, TimeSeries
from ninja import ModelSchema, Schema


class SynergyResultSchema(ModelSchema):
    class Meta:
        model = SynergyResult
        fields = "__all__"


class SourceSchema(ModelSchema):
    class Meta:
        model = Source
        fields = "__all__"


class TimeSeriesSchema(ModelSchema):
    class Meta:
        model = TimeSeries
        fields = "__all__"


class ResourceVariableSchema(ModelSchema):
    time_series: TimeSeriesSchema | None = None

    class Meta:
        model = ResourceVariable
        fields = "__all__"


class SiteSchema(ModelSchema):
    resources: list[ResourceVariableSchema] | None = []

    class Meta:
        model = Site
        fields = "__all__"


class SiteCreateSchema(Schema):
    name: str
    description: str
    latitude: float
    longitude: float
    elevation: float
    resources: list[int]


class SitePatchSchema(Schema):
    resource_id: int


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
