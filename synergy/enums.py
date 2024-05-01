from enum import Enum


class ResourceEnum(Enum):
    HYDRO = "hydro"
    SOLAR = "solar"
    WIND = "wind"
    BIOMASS = "biomass"


class DimensionEnum(Enum):
    SOCIAL = "social"
    ECONOMIC = "economic"
    ENVIRONMENTAL = "environmental"
    TECHNICAL = "technical"
