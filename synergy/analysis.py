from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class Analysis(BaseModel):
    analysis_id: int
    name: str
    description: str
    site_id: int
    demand: float
    seed_alternatives: str
    total_alternatives: int
    date_created: datetime
    date_updated: datetime


class SynergyResult(BaseModel):
    result_id: int
    analysis_id: int
    scenario_id: int
    total_installed_capacity: float
    date_created: datetime
    date_updated: datetime


class Scenario(BaseModel):
    scenario_id: int
    name: str
    description: str
    criteria_weight: dict
    subcriteria_weight: dict


class Site(BaseModel):
    site_id: int
    name: str
    description: str
    latitude: float
    longitude: float
    elevation: float
    resources_description: str


class SiteAttribute(BaseModel):
    site_attribute_id: int
    site_id: int
    attribute_id: int
    name: str
    value: float
    description: str
