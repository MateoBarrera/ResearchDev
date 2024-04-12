from enum import Enum

from pytz import HOUR


class Unit(Enum):
    METER_PER_SECOND = "m/s"
    CUBIT_METER = "m^3/s"
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"


class Frequency(Enum):
    HOURLY = "Hourly"
    DAILY = "Daily"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"


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
