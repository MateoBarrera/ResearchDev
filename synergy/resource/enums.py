from enum import Enum


class Unit(Enum):
    METER_PER_SECOND = "m/s"
    CUBIT_METER = "m³"
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"


class ResourceType(Enum):
    Hydro = "Hydro"
    Solar = "Solar"
    Wind = "Wind"
    Biomass = "Biomass"


class Dimension(Enum):
    SOCIAL = "Social"
    ECONOMIC = "Economic"
    ENVIRONMENTAL = "Environmental"
    TECHNICAL = "Technical"


class CriteriaType(Enum):
    COST = "Cost"
    BENEFIT = "Benefit"
