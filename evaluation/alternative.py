"""Alternative file

This module include the class for generate the scenarios/alternatives specifications

Autor: Mateo Barrera
Date: 11-03-2023
"""
from operator import length_hint
import numpy as np
import pandas as pd
from itertools import product
from prettytable import PrettyTable


class Alternatives:
    def __init__(
        self,
        resources_included=[1, 1, 1, 1],
        seed=[1.0, 0.5, 0.25, 0],
        installed_capacity=100,
    ) -> None:
        """_summary_

        Args:
            resources_included (list, optional): _description_. Defaults to [1, 1, 1, 1].
            seed (list, optional): _description_. Defaults to [1.0, 0.5, 0.25, 0].
            installed_capacity (int, optional): _description_. Defaults to 100.
        """
        self.resources_included = resources_included
        self.seed = seed
        self.installed_capacity = installed_capacity
        self.alternatives, self.scenarios = self.__generate_scenarios()
        # return self.alternatives

    def __str__(self) -> str:
        return self.__describe_scenarios()

    def get(self):
        return self.alternatives

    def __generate_scenarios(self):
        """_summary_

        Args:
            resources_included (list, optional): _description_. Defaults to [1, 1, 1, 1].

        Returns:
            _type_: _description_
        """
        (
            solar_inclusion,
            wind_inclusion,
            hydro_inclusion,
            biomass_inclusion,
        ) = self.resources_included

        all_combinations = list(product(*[self.seed] * 4))

        weight_scenarios = np.array(all_combinations)
        y_resources = np.array(
            [solar_inclusion, wind_inclusion, hydro_inclusion, biomass_inclusion]
        )

        scenario_matrix = weight_scenarios * y_resources
        scenario_array = list()
        for items in scenario_matrix:
            if sum(items) == 1:
                scenario_array.append(str(list(items)))

        scenario_array = list(dict.fromkeys(scenario_array))
        scenario_array = [eval(i) for i in scenario_array]

        # self.__describe_scenarios(scenario_array)
        alternatives = pd.DataFrame(
            columns=["solar", "wind", "hydro", "biomass"], data=scenario_array
        )
        return alternatives, scenario_array

    def __describe_scenarios(self):
        """_summary_

        Args:
            scenarios (_type_): _description_
            resources_included (_type_): _description_
            seed (_type_): _description_
        """
        info = PrettyTable()
        info.title = "ALTERNATIVES SUMMARY"
        info.field_names = ["TARGET CAPACITY ", f"{self.installed_capacity} kW"]
        info.add_row(["---------------------", "-----------"])
        info.add_row(["TOTAL ALTERNATIVES", "{}".format(len(self.scenarios))])
        info.add_row(["---------------------", "-----------"])
        info.add_row(["RESOURCES", "INCLUDED"])
        for resource in zip(
            ["solar", "wind", "hydro", "biomass"], self.resources_included
        ):
            if resource[1] == 1:
                info.add_row([resource[0], "\N{check mark}"])
            else:
                info.add_row([resource[0], "\N{Ballot X}"])
        info.add_row(["---------------------", "-----------"])
        text = ["% VARIATIONS FOR", "INSTALLED CAPACITY", "TARGET"] + [
            " " for _ in range(len(self.seed) - 3)
        ]
        for index, x in enumerate(self.seed):
            info.add_row([text[index], f"{x*100} %"])
        # info.add_row(["{} %".format(x * 100) for x in self.seed])
        scenario_matrix = PrettyTable()
        scenario_matrix.field_names = ["solar", "wind", "hydro", "biomass"]
        scenario_matrix.title = "ALTERNATIVES"
        for scenario in self.scenarios:
            scenario = list(map(lambda x: "{} %".format(x * 100), scenario))
            scenario_matrix.add_row(scenario)

        return f"\n{info}\n{scenario_matrix}"


if __name__ == "__main__":
    alternatives = Alternatives()
    print(alternatives)
    df_alternatives = alternatives.get()
    print(df_alternatives)
