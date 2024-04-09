from enum import Enum

from evaluation.resource.resource import Biomass, Hydro, Wind


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
