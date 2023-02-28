"""_summary_
"""
import numpy as np
import pandas as pd  # pylint: disable=import-error
from prettytable import PrettyTable  # pylint: disable=import-error
import json


class Indicator:
    """_summary_"""

    __id: str
    __name: str
    __description: str
    __source: str
    __data: None
    __year: str
    __type_indicator: str
    __raw_data: json

    def __init__(self, file) -> None:
        self.__raw_data = "#"
        self.__id = file["id"]
        self.__name = file["name"]
        self.__description = file["description"]
        self.__source = file["source"]
        self.__year = file["year"]
        self.type_indicator = file["type_indicator"]
        self.__raw_data = json.load(file)

    @property
    def id(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__id

    @property
    def name(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__name

    @property
    def source(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__source

    @property
    def description(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__description

    @property
    def data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__data

    @property
    def year(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__year

    @property
    def type_indicator(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__type_indicator

    @property
    def json(self):
        return self.__raw_data

    @json.setter
    def json(self, data: str):
        """_summary_

        Args:
            path (str): _description_
        """
        print(data)


class Indicators:
    __ambiental_indicators: list
    __economic_indicators: list
    __tecnical_indicators: list

    def __init__(self) -> None:
        self.__ambiental_indicators = list()

    def __str__(self) -> str:
        return str(self.__ambiental_indicators)

    @property
    def ambiental(self):
        return self.__ambiental_indicators

    def __validate_json(self, file):
        keys_expected = [
            "id",
            "name",
            "criteria",
            "description",
            "source",
            "data",
            "year",
            "unit",
            "type_indicator",
        ]
        if keys_expected != list(file.keys()):
            key = file["id"]
            raise KeyError(f"json file format is corrupted: key value = {key}")
        return True

    def load(self, path: str):
        """_summary_

        Args:
            path (str): _description_
        """
        with open(path, "r") as file:
            file_data = json.load(file)
        file.close()
        for count, item in enumerate(file_data):
            if self.__validate_json(file_data[item]):
                self.__ambiental_indicators.append(file_data[item])

    def add_formula(self):
        __funtions_indicators = {
            "101": {
                "formula": lambda solar, wind: solar + wind,
            },
            "102": {
                "formula": lambda solar, wind: solar + wind,
            },
        }
        for count, item in enumerate(__funtions_indicators):
            try:
                self.__ambiental_indicators[count].update(
                    {"formula": __funtions_indicators[item]["formula"]}
                )
            except:
                continue

    def evaluate_alternative(self, alternatives):
        funtions_indicators = {
            "101": {
                "id": "C1.1",
                "formula": lambda x: 0.367
                * (
                    x["solar_generation"] * 0.20
                    + x["wind_generation"] * 0.25
                    + x["hydro_generation"] * 0.35
                    # + x["biomass_generation"] * 0.70
                ),
            },
            "102": {
                "id": "C1.2",
                "formula": lambda x: (
                    (x["solar_generation"] / (8760 * 1000)) * 0.33
                    + (x["wind_generation"] / (8760 * 1000)) * 1.57
                    + (x["hydro_generation"] / (8760 * 1000)) * 0.02
                    # + (x["biomass_generation"] / (8760 * 1000)) * 12.65
                ),
            },
            "102": {
                "id": "C1.2",
                "formula": lambda x: (
                    (x["solar_generation"] / (8760 * 1000)) * 0.33
                    + (x["wind_generation"] / (8760 * 1000)) * 1.57
                    + (x["hydro_generation"] / (8760 * 1000)) * 0.02
                    # + (x["biomass_generation"] / (8760 * 1000)) * 12.65
                ),
            },
            "104": {
                "id": "C1.4",
                "formula": lambda x: (
                    (x["solar_generation"] / (8760 * 1000)) * 0.001
                    + (x["wind_generation"] / (8760 * 1000)) * 5.4e-5
                    + (x["hydro_generation"] / (8760 * 1000)) * 8.9e-6
                    # + (x["biomass_generation"] / (8760 * 1000)) * 1.55
                ),
            },
            "201": {
                "id": "C2.1",
                "formula": lambda x: (
                    (
                        (x["solar_generation"] / (8760 * 1000)) * 202.94
                        + (x["wind_generation"] / (8760 * 1000)) * 76.28
                        + (x["hydro_generation"] / (8760 * 1000)) * 124.97
                        # + (x["biomass_generation"] / (8760 * 1000)) * 72
                    )
                    / (
                        x["solar_generation"] / (8760 * 1000)
                        + x["wind_generation"] / (8760 * 1000)
                        + x["hydro_generation"] / (8760 * 1000)
                        # + (x["biomass_generation"]/(8760 * 1000)
                    )
                ),
            },
            "202": {
                "id": "C2.2",
                "formula": lambda x: (
                    (
                        x["solar"] * 1100
                        + x["wind"] * 1350
                        + x["hydro"] * 29900
                        # + x["biomass"] * 2000
                    )
                    / (
                        x["solar"]
                        + x["wind"]
                        + x["hydro"]
                        # + x["biomass"]
                    )
                ),
            },
            "203": {
                "id": "C2.3",
                "formula": lambda x: (
                    (
                        x["solar"] * 6.5
                        + x["wind"] * 40
                        + x["hydro"] * 37
                        # + (x["biomass"] * 21
                    )
                    / (
                        x["solar"]
                        + x["wind"]
                        + x["hydro"]
                        # + x["biomass"]
                    )
                ),
            },
            "301": {
                "id": "C3.1",
                "formula": lambda x: (
                    (
                        x["solar"] * 0.25
                        + x["wind"] * 0.40
                        + x["hydro"] * 0.89
                        # + (x["biomass"] * .35
                    )
                    / (
                        x["solar"]
                        + x["wind"]
                        + x["hydro"]
                        # + x["biomass"]
                    )
                ),
            },
            "302": {
                "id": "C3.2",
                "formula": lambda x: (
                    (
                        x["solar"] * 0
                        + x["wind"] * 0
                        + x["hydro"] * 0
                        # + (x["biomass"] * 0.5
                    )
                    / (
                        x["solar"]
                        + x["wind"]
                        + x["hydro"]
                        # + x["biomass"]
                    )
                ),
            },
            "303": {
                "id": "C3.3",
                "formula": lambda x: (
                    (
                        x["solar"] * 1
                        + x["wind"] * 0.6667
                        + x["hydro"] * 0.8333
                        # + (x["biomass"] * .35
                    )
                    / (
                        x["solar"]
                        + x["wind"]
                        + x["hydro"]
                        # + x["biomass"]
                    )
                ),
            },
        }
        for indicator in funtions_indicators.values():
            alternatives[indicator["id"]] = alternatives.apply(
                indicator["formula"], axis=1
            )
        print(":: Alternatives  ::")
        print(alternatives.iloc[:, :6].to_markdown(floatfmt=".2f"))
        print(":: Installed Capacity [kW]; Generation [kW year]  ::")
        print("\n:: Criteria  ::")
        print(alternatives.iloc[:, 7:].to_markdown(floatfmt=".4f"))
        return alternatives.iloc[:, 7:]


if __name__ == "__main__":
    ind = Indicators()
    ind.load("Evaluation/Indicator/indicators.json")
    # print(ind)
    # ind.add_formula()
    # print(ind.ambiental[0]["formula"])
    ["solar", "wind", "hydro", "biomass"]
    df = pd.DataFrame(
        {
            "solar": [1, 0.5, 0],
            "wind": [0, 0.5, 0.5],
            "hydro": [0, 0, 0.25],
            "biomass": [0, 0, 0.25],
        }
    )
    print(df)
    ind.evaluate_alternative(df)
    # df = df.apply(ind.ambiental[0]["formula"], axis=1)
    # print(ind.ambiental[0]["formula"](solar=12, wind=2))
