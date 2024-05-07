""" class Historical(BaseModel):
    date: str
    source: str


class Resource(BaseModel):
    name: str
    capacity: float
    ubication: str
    is_viability: Optional[bool] = False
    historical: List[Historical]

from typing import List
from datetime import datetime
from pydantic import BaseModel
from .enums import ResourceType, Unit


# New clases definition
class Resource(BaseModel):
    resource_is: int
    site_id: int
    name: str
    resource_type: ResourceType
    description: str


class ResourceVariable(BaseModel):
    variable_id: int
    name: str
    unit: Unit
    source: str
    frequency: str
    date_added: datetime
    date_updated: datetime


class TimeSerie(BaseModel):
    variable_id: int
    time_stamp: datetime
    value: float


class BaseHistoricalData(BaseModel):
    timestamp: datetime
    energy_production: float
    capacity: float


class SolarPanelHistoricalData(BaseHistoricalData):
    temperature: float
    efficiency: float


class WindTurbineHistoricalData(BaseHistoricalData):
    wind_speed: float
    blade_length: float


class RenewableResource(BaseModel):
    name: str
    description: str
    location: str
    current_capacity: float
    historical_data: List[BaseHistoricalData] = []

    def add_historical_data(
        self, timestamp: datetime, energy_production: float, capacity: float
    ):
        historical_entry = BaseHistoricalData(
            timestamp=timestamp, energy_production=energy_production, capacity=capacity
        )
        self.historical_data.append(historical_entry)


# Example usage
if __name__ == "__main__":
    solar_panels = RenewableResource(
        name="Solar Panels",
        description="Photovoltaic solar panels",
        location="Rooftop",
        current_capacity=100.0,
    )

    # Add solar panel historical data
    solar_panels.add_historical_data(
        timestamp=datetime(2024, 3, 20, 12, 0), energy_production=80.0, capacity=100.0
    )

    # Create a wind turbine resource
    wind_turbine = RenewableResource(
        name="Wind Turbine",
        description="Large wind turbine",
        location="Open field",
        current_capacity=500.0,
    )

    # Add wind turbine historical data
    wind_turbine.add_historical_data(
        timestamp=datetime(2024, 3, 20, 12, 0), energy_production=300.0, capacity=500.0
    )

    # Print historical data for both resources
    print("Solar Panels Historical Data:")
    for entry in solar_panels.historical_data:
        print(
            f"Timestamp: {entry.timestamp}, Energy Production: {entry.energy_production} kWh, Capacity: {entry.capacity} kW"
        )

    print("\nWind Turbine Historical Data:")
    for entry in wind_turbine.historical_data:
        print(
            f"Timestamp: {entry.timestamp}, Energy Production: {entry.energy_production} kWh, Capacity: {entry.capacity} kW"
        )
"""

import numpy as np
import pandas as pd
import statistics
from pydantic import BaseModel, validator
from typing import Dict, List
from .enums import ResourceType, Unit, Frequency, VariableEnum
from .utils.csv_readers import load_csv, load_excel


class ResourceVariable(BaseModel):
    name: VariableEnum = None
    type_resource: ResourceType = None
    source: str = None
    unit: Unit = None
    frequency: Frequency = None
    data: Dict[str, float] = {}

    def __init__(
        self,
        file_csv: str = None,
        file_excel: str = None,
        **data,
    ):
        if file_csv:
            data = load_csv(file_csv)
        elif file_excel:
            data = load_excel(file_excel)
        super().__init__(**data)

    @property
    def data(self):
        return self.data


class Resource(BaseModel):
    name: str
    type_resource: ResourceType
    variables: List[ResourceVariable] = []

    @validator("variables")
    def validate_variables(cls, v):
        for variable in v:
            if variable.type_resource != cls.type_resource:
                raise ValueError("The variable type does not match the resource type")
        return v

    def __init__(self, **data):
        super().__init__(**data)

    def add_variable(self, variable: ResourceVariable):
        if variable.type_resource != self.type_resource:
            raise ValueError("The variable type does not match the resource type")
        self.variables.append(variable)

    def set_viability(self, value):
        self.__viability = value

    def set_variability(self, value):
        self.__variability = value

    def set_autonomy(self, value):
        self.__autonomy = value

    @property
    def viability(self):
        return self.__viability

    @property
    def variability(self):
        return self.__variability

    @property
    def autonomy(self):
        return self.__autonomy


class Hydro(Resource):
    def __init__(self, **data):
        super().__init__(type_resource=ResourceType.HYDRO, **data)

    def evaluate(self, installed_capacity: float):
        primary_variable = next(
            (v for v in self.variables if v.name == VariableEnum.FLOW_RIVER), None
        )
        if not primary_variable:
            raise ValueError("Primary variable not found")

        self.set_variability(
            statistics.stdev(primary_variable.data.values())
            / statistics.mean(primary_variable.data.values())
        )
        return installed_capacity * 0.8


class Solar(Resource):
    def __init__(self, **data):
        super().__init__(type_resource=ResourceType.SOLAR, **data)

    def evaluate(self, installed_capacity: float):
        primary_variable = next(
            (v for v in self.variables if v.name == VariableEnum.SOLAR_IRRADIANCE), None
        )
        if not primary_variable:
            raise ValueError("Primary variable not found")

        self.set_variability(
            statistics.stdev(primary_variable.data.values())
            / statistics.mean(primary_variable.data.values())
        )
        return installed_capacity * 0.8


class Wind(Resource):
    def __init__(self, **data):
        super().__init__(type_resource=ResourceType.WIND, **data)

    def evaluate(self, installed_capacity: float):
        primary_variable = next(
            (v for v in self.variables if v.name == VariableEnum.WIND_SPEED), None
        )
        if not primary_variable:
            raise ValueError("Primary variable not found")

        self.set_variability(
            statistics.stdev(primary_variable.data.values())
            / statistics.mean(primary_variable.data.values())
        )
        return installed_capacity * 0.8
