from datetime import datetime
import resource
from numpy import source
from pydantic import BaseModel
from typing import Optional, List
from .resources.enums import Unit, Dimension, CriteriaType


class Criteria(BaseModel):
    criteria_id: int
    name: str
    description: str
    dimension: Dimension
    source: str
    criteria_type: CriteriaType
    criteria_unit: Unit


class CriteriaData(BaseModel):
    criteria_data_id: int
    criteria_id: int
    resource_id: int
    value: float
    date: datetime
