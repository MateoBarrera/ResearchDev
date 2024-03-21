from pydantic import BaseModel
from typing import Optional


class Resource(BaseModel):
    name: str
    type: str
    capacity: float
    ubication: str
    is_operative: Optional[bool] = False
    is_viability: Optional[bool] = False
