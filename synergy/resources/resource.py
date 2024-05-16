import numpy as np
import pandas as pd
import statistics
import math
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

    def add_variables(self, file_excel: str):
        data_variables = load_excel(file_excel)
        print("2" * 100)
        for variable in data_variables:
            print(type(variable))
            variable_resource = ResourceVariable(**variable)
            print(variable_resource)
            self.add_variable(variable_resource)

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

    _panel_capacity: float = 100  # in watts
    _num_panels: int = 100

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

        self._num_panels = math.ceil(installed_capacity / self._panel_capacity)

        df = pd.DataFrame(index=values_per_month.index)
        df["PSH"] = values_per_month.mean(axis=1)
        df["days"] = DAYS_PER_MONTH

        df["monthly energy"] = (
            df["PSH"]
            * self._num_panels
            * self._panel_capacity
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
        for key, value in values.items():
            if hasattr(self, f"_{key}"):
                setattr(self, f"_{key}", value)
            else:
                raise ValueError(f"Unknown attribute: {key}")


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

        self._num_turbines = math.ceil(installed_capacity / self._rated_power)

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
        raise NotImplementedError

    @wind_params.setter
    def wind_params(self, values: dict):
        for key, value in values.items():
            if hasattr(self, f"_{key}"):
                setattr(self, f"_{key}", value)
            else:
                raise ValueError(f"Unknown attribute: {key}")


class Hydro(Resource):
    """
    A class representing a Hydro resource.

    Attributes:
        type_resource (ResourceType): The type of the resource.
        data (dict): Additional data for the resource.

    Methods:
        evaluate(self, installed_capacity: float): Evaluates the Wind resource.

    """

    name: str
    _head = 2  # in meters
    _turbine_efficiency = 0.80  # efficiency of the hydro power plant
    _capacity_factor = 0.4  # in percentage
    _rated_power = 100  # in kilowatts (rated power of a single turbine)
    _num_turbines = 1  # total number of turbines

    _design_flow_rate = 3  # in cubic meters per second
    _ecological_flow = None  # in cubic meters per second
    _q_sr = 0  # in cubic meters per second

    def __init__(self, **data):
        """
        Initializes a Resource object.

        Args:
            data (dict): A dictionary containing the data for the resource.

        The `data` argument in the constructor should be a dictionary containing the necessary information for a Resource instance. The keys should be the attribute names and the values should be the corresponding values. For example:

        data = {
            'name': 'Hydro',
            'type_resource': ResourceType.HYDRO,
            'variables': [ResourceVariable(...), ...]
        }
        resource = Resource(**data)
        """
        super().__init__(type_resource=ResourceType.HYDRO, **data)

    def get_potential(self, values_per_month, installed_capacity) -> float:

        self._num_turbines = math.ceil(installed_capacity / self._rated_power)

        df = pd.DataFrame(index=values_per_month.index)
        df["flow_rate"] = values_per_month.mean(axis=1)
        df["flow_rate"] = df["flow_rate"] - self._ecological_flow
        df.loc[df["flow_rate"] > self._design_flow_rate, "flow_rate"] = (
            self._design_flow_rate
        )
        df.loc[df["flow_rate"] < 0, "flow_rate"] = 0

        df["days"] = DAYS_PER_MONTH
        df["monthly energy"] = (
            9.81
            * 0.997
            * self._head
            * self._turbine_efficiency
            * df["flow_rate"]
            * self._capacity_factor
            * self._rated_power
            * self._num_turbines
            * df["days"]
        )

        power_generation = df["monthly energy"].sum()
        df = df.drop(columns=["days"])
        if True:
            capacity_factor = power_generation / (installed_capacity * 365 * 24)
            print("\n:: Hydro ::")
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
            (v for v in self.variables if v.name == VariableEnum.FLOW_RIVER), None
        )
        if not primary_variable:
            raise ValueError(f"Primary variable {VariableEnum.FLOW_RIVER} not found")

        self.set_variability(
            statistics.stdev(primary_variable.data.values())
            / statistics.mean(primary_variable.data.values())
        )
        values_per_date, values_per_month = format_values(primary_variable.data)
        data_sort = np.sort(values_per_date["value"])[::-1]
        index_q_sr = int(len(data_sort) * 0.7)
        self._ecological_flow = data_sort[index_q_sr]
        result = self.get_potential(values_per_month, installed_capacity)

        return result

    @property
    def hydro_params(self):
        raise NotImplementedError

    @hydro_params.setter
    def hydro_params(self, values: dict):
        for key, value in values.items():
            if hasattr(self, f"_{key}"):
                setattr(self, f"_{key}", value)
            else:
                raise ValueError(f"Unknown attribute: {key}")


class Biomass(Resource):
    """
    A class representing a solar resource.

    Attributes:
        type_resource (ResourceType): The type of the resource.
        data (dict): Additional data for the resource.

    Methods:
        evaluate(self, installed_capacity: float): Evaluates the solar resource.

    """

    name: str
    _biomass_sources: Dict[str, float] = {}
    _collection_efficiency: float = 0.80
    _cell_fuel_efficiency: float = 0.90
    _cells_capacity: float = 100
    _num_cells: int = 1
    _pci: float = 4.77  # Lower caloric potential in kWh/m3

    def __init__(self, **data):
        """
        Initializes a Resource object.

        Args:
            data (dict): A dictionary containing the data for the resource.

        The `data` argument in the constructor should be a dictionary containing the necessary information for a Resource instance. The keys should be the attribute names and the values should be the corresponding values. For example:

        data = {
            'name': 'Biomass',
            'type_resource': ResourceType.BIOMASS,
            'variables': [ResourceVariable(...), ...]
        }
        resource = Resource(**data)
        """
        super().__init__(type_resource=ResourceType.BIOMASS, **data)

    def get_useful_biomass(self, raw_biomass) -> dict:
        factors_useful_biomass = {
            "sugar_cane": 0.5,
            "rice_husk": 0.3,
            "rice_straw": 0.2,
        }
        useful_biomass = {}
        for key, value in raw_biomass.items():
            useful_biomass[key] = factors_useful_biomass[key] * value
        return useful_biomass

    def get_potential(self, useful_biomass, installed_capacity) -> float:

        self._num_cells = math.ceil(installed_capacity / self._cells_capacity)

        """df = pd.DataFrame(useful_biomass)

        df["monthly energy"] = (
            df["PSH"]
            * self._num_panels
            * self._panel_capacity
            * self._efficiency
            * df["days"]
            * self._temperature_factor
            * self._weather_factor
        )

        power_generation = df["monthly energy"].sum()
        df = df.drop(columns=["days"])
        if True:
            capacity_factor = power_generation / (installed_capacity * 365 * 24)
            print("\n:: Biomass ::")
            print(df.to_markdown(floatfmt=".1f"))
            print(
                f"Generation {round(power_generation, 2)}[kWh year]; Capacity Factor {round(capacity_factor * 100, 2)}%"
            )"""
        return self._num_cells

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
        result = self.get_potential(
            self.get_useful_biomass(self.raw_biomass),
            installed_capacity=installed_capacity,
        )

        return result

    @property
    def biomass_sources(self):
        return self._biomass_sources

    @biomass_sources.setter
    def biomass_sources(self, values: dict):
        self._biomass_sources = values

    @property
    def biomass_params(self):
        raise NotImplementedError

    @biomass_params.setter
    def biomass_params(self, values: dict):
        for key, value in values.items():
            if hasattr(self, f"_{key}"):
                setattr(self, f"_{key}", value)
            else:
                raise ValueError(f"Unknown attribute: {key}")
