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

from bdb import effective
import numpy as np
import pandas as pd
import statistics
from pydantic import BaseModel, validator
from typing import Dict, List
from .enums import ResourceType, Unit, Frequency, VariableEnum
from .utils.csv_readers import load_csv, load_excel, format_values

DAYS_PER_MONTH: List[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class ResourceVariable(BaseModel):
    """
    Represents a resource variable.

    Attributes:
        name (VariableEnum): The name of the variable.
        type_resource (ResourceType): The type of the resource.
        source (str): The source of the resource.
        unit (Unit): The unit of measurement for the resource.
        frequency (Frequency): The frequency at which the resource is measured.
        data (Dict[str, float]): The data associated with the resource.

    Methods:
        data: Returns the data associated with the resource.

    """

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
        """
        Initializes a new instance of the ResourceVariable class.

        Args:
            file_csv (str): The path to a CSV file containing data for the resource.
            file_excel (str): The path to an Excel file containing data for the resource.
            **data: Additional data for the resource.

        """
        if file_csv:
            data = load_csv(file_csv)
        elif file_excel:
            data = load_excel(file_excel)
        super().__init__(**data)

    @property
    def data(self):
        """
        Returns the data associated with the resource.

        Returns:
            Dict[str, float]: The data associated with the resource.

        """
        return self.data


class Resource(BaseModel):
    """
    Represents a resource.

    Attributes:
        name (str): The name of the resource.
        type_resource (ResourceType): The type of the resource.
        variables (List[ResourceVariable]): The list of variables associated with the resource.

    Methods:
        add_variable(variable: ResourceVariable): Adds a variable to the resource.
        set_viability(value): Sets the viability of the resource.
        set_variability(value): Sets the variability of the resource.
        set_autonomy(value): Sets the autonomy of the resource.
        viability: Gets the viability of the resource.
        variability: Gets the variability of the resource.
        autonomy: Gets the autonomy of the resource.


    The `data` argument in the constructor should be a dictionary containing the necessary information for a Resource instance. The keys should be the attribute names and the values should be the corresponding values. For example:

    data = {
        'name': 'Solar',
        'type_resource': ResourceType.SOLAR,
        'variables': [ResourceVariable(...), ...]
    }
    resource = Resource(**data)
    """

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


class Solar(Resource):
    """
    A class representing a solar resource.

    Attributes:
        type_resource (ResourceType): The type of the resource.
        data (dict): Additional data for the resource.

    Methods:
        evaluate(self, installed_capacity: float): Evaluates the solar resource.

    """

    name: str
    _efficiency: float = 0.90
    _temperature_factor: float = 0.95
    _weather_factor: float = 1.0

    def __init__(self, **data):
        """
        Initializes a Resource object.

        Args:
            data (dict): A dictionary containing the data for the resource.

        The `data` argument in the constructor should be a dictionary containing the necessary information for a Resource instance. The keys should be the attribute names and the values should be the corresponding values. For example:

        data = {
            'name': 'Solar',
            'type_resource': ResourceType.SOLAR,
            'variables': [ResourceVariable(...), ...]
        }
        resource = Resource(**data)
        """
        super().__init__(type_resource=ResourceType.SOLAR, **data)

    def get_potential(self, values_per_month, installed_capacity) -> float:
        df = pd.DataFrame(index=values_per_month.index)
        df["PSH"] = values_per_month.mean(axis=1)
        df["days"] = DAYS_PER_MONTH

        df["monthly energy"] = (
            df["PSH"]
            * installed_capacity
            * self._efficiency
            * df["days"]
            * self._temperature_factor
            * self._weather_factor
        )

        # Monthly temperature and weather association
        # df["monthly energy"] = (
        #    df["PSH"]
        #    * installed_capacity
        #    * self._efficiency
        #    * df["days"]
        #    * df["temperature_factor"]
        #    * df["weather_factor"]
        # )

        power_generation = df["monthly energy"].sum()
        df = df.drop(columns=["days"])
        if True:
            capacity_factor = power_generation / (installed_capacity * 365 * 24)
            print("\n:: Solar ::")
            print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kWh year]; Capacity Factor {round(capacity_factor * 100, 2)}%"
            )
        return power_generation

    def evaluate(self, installed_capacity: float):
        """
        Evaluates the solar resource.

        Args:
            installed_capacity (float): The installed capacity of the solar resource.

        Returns:
            float: The evaluated value based on the installed capacity.

        Raises:
            ValueError: If the primary variable is not found.

        """
        primary_variable = next(
            (v for v in self.variables if v.name == VariableEnum.SOLAR_IRRADIANCE), None
        )
        if not primary_variable:
            raise ValueError(
                f"Primary variable {VariableEnum.SOLAR_IRRADIANCE} not found"
            )

        self.set_variability(
            statistics.stdev(primary_variable.data.values())
            / statistics.mean(primary_variable.data.values())
        )
        values_per_date, values_per_month = format_values(primary_variable.data)
        result = self.get_potential(values_per_month, installed_capacity)

        return result

    @property
    def solar_params(self):
        return {
            "efficiency": self._efficiency,
            "temperature_factor": self._temperature_factor,
            "weather_factor": self._weather_factor,
        }

    @solar_params.setter
    def solar_params(self, values: dict):
        self._efficiency = values["efficiency"]
        self._temperature_factor = values["temperature_factor"]
        self._weather_factor = values["weather_factor"]


class Wind(Resource):
    """
    A class representing a wind resource.

    Attributes:
        type_resource (ResourceType): The type of the resource.
        data (dict): Additional data for the resource.

    Methods:
        evaluate(self, installed_capacity: float): Evaluates the Wind resource.

    """

    name: str
    _swept_area = 100  # in square meters
    _air_density = 1.225  # in kg/m^3 (typical value at sea level)
    _average_wind_speed = 6  # in meters per second
    _capacity_factor = 0.30  # in percentage
    _rated_power = 1000  # in kilowatts (rated power of a single turbine)
    _num_turbines = 50  # total number of turbines in the wind farm

    def __init__(self, **data):
        """
        Initializes a Resource object.

        Args:
            data (dict): A dictionary containing the data for the resource.

        The `data` argument in the constructor should be a dictionary containing the necessary information for a Resource instance. The keys should be the attribute names and the values should be the corresponding values. For example:

        data = {
            'name': 'Wind',
            'type_resource': ResourceType.WIND,
            'variables': [ResourceVariable(...), ...]
        }
        resource = Resource(**data)
        """
        super().__init__(type_resource=ResourceType.WIND, **data)

    def get_potential(self, values_per_month, installed_capacity) -> float:

        self._num_turbines = installed_capacity // self._rated_power

        df = pd.DataFrame(index=values_per_month.index)
        df["wind_sp"] = values_per_month.mean(axis=1)
        df["days"] = DAYS_PER_MONTH

        df["monthly energy"] = (
            (0.5 * self._air_density * self._swept_area * df["wind_sp"] ** 3 / 1000)
            * self._rated_power
            * self._num_turbines
            * self._capacity_factor
            * df["days"]
        )

        # Monthly temperature and weather association
        # df["monthly energy"] = (
        #    df["PSH"]
        #    * installed_capacity
        #    * self._efficiency
        #    * df["days"]
        #    * df["temperature_factor"]
        #    * df["weather_factor"]
        # )

        power_generation = df["monthly energy"].sum()
        df = df.drop(columns=["days"])
        if True:
            capacity_factor = power_generation / (installed_capacity * 365 * 24)
            print("\n:: Wind ::")
            print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kWh year]; Capacity Factor {round(capacity_factor * 100, 2)}%"
            )
        return power_generation

    def evaluate(self, installed_capacity: float):
        """
        Evaluates the solar resource.

        Args:
            installed_capacity (float): The installed capacity of the solar resource.

        Returns:
            float: The evaluated value based on the installed capacity.

        Raises:
            ValueError: If the primary variable is not found.

        """
        primary_variable = next(
            (v for v in self.variables if v.name == VariableEnum.WIND_SPEED), None
        )
        if not primary_variable:
            raise ValueError(f"Primary variable {VariableEnum.WIND_SPEED} not found")

        self.set_variability(
            statistics.stdev(primary_variable.data.values())
            / statistics.mean(primary_variable.data.values())
        )
        values_per_date, values_per_month = format_values(primary_variable.data)
        result = self.get_potential(values_per_month, installed_capacity)

        return result

    @property
    def wind_params(self):
        return True

    @wind_params.setter
    def wind_params(self, values: dict):
        pass
