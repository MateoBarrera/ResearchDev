from enum import Enum
from pickle import POP


class Unit(Enum):
    METER_PER_SECOND = "m/s"
    CUBIT_METER = "m³"
    CUBIT_METERS_PER_SECOND = "m³/s"
    CUBIT_METERS_PER_DAY = "m³/day"
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"
    KW = "kW"
    IRRADIANCE = "kW-hr/m^2/day"
    HECTARE = "ha"
    POPULATION = "population"


class ResourceType(Enum):
    HYDRO = "Hydro"
    SOLAR = "Solar"
    WIND = "Wind"
    BIOMASS = "Biomass"


class VariableEnum(Enum):
    FLOW_RIVER = "Flow river"
    WIND_SPEED = "Wind speed"
    BIOGAS = "Biogas"
    SOLAR_IRRADIANCE = "Solar irradiance"
    TEMPERATURE = "Solar temperature"
    RICE = "Arroz"
    COFFEE = "Café"
    BANANA = "Plátano"
    CITRUS = "Cítricos"
    SUGAR_CANE = "Caña"
    CATTLE = "bovino"
    PINEAPPLE = "Piña"


class Frequency(Enum):
    HOURLY = "Hourly"
    DAILY = "Daily"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"


class Dimension(Enum):
    SOCIAL = "Social"
    ECONOMIC = "Economic"
    ENVIRONMENTAL = "Environmental"
    TECHNICAL = "Technical"


class CriteriaType(Enum):
    COST = "Cost"
    BENEFIT = "Benefit"
