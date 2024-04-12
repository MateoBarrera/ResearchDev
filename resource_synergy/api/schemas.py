from sqlite3 import Time
from .models import Analysis, SynergyResult, Site, ResourceVariable, Source
from ninja import ModelSchema, Schema
from pydantic import BaseModel, validator
from typing import List
from datetime import datetime


class SynergyResultSchema(ModelSchema):
    class Meta:
        model = SynergyResult
        fields = "__all__"


class SourceSchema(ModelSchema):
    class Meta:
        model = Source
        fields = "__all__"


class TimeSerieItem(BaseModel):
    time_stamp: datetime
    value: float


class ResourceVariableSchema(ModelSchema):
    time_series: List[TimeSerieItem] | None = []

    class Meta:
        model = ResourceVariable
        fields = "__all__"

    @validator("time_series", each_item=True)
    def validate_time_series(cls, value):
        if not isinstance(value, TimeSerieItem):
            raise ValueError("Time series must be a TimeSeriesItem")
        return value


class SiteSchema(ModelSchema):
    resources: List[ResourceVariableSchema] | None = []

    class Meta:
        model = Site
        fields = "__all__"


class SiteCreateSchema(Schema):
    name: str
    description: str
    latitude: float
    longitude: float
    elevation: float
    resources: List[int] | None = None


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
