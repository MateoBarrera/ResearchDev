import re
import pandas as pd
from pydantic import BaseModel
from typing import Dict, List, Any
from .enums import ResourceEnum, DimensionEnum
import numexpr as ne


class Indicator(BaseModel):
    id: int
    name: str
    dimension: DimensionEnum
    description: str
    source: str
    data: Dict[ResourceEnum, float]
    year: str
    unit: str
    type_indicator: str
    formula: str

    def __init__(self, **data):
        super().__init__(**data)

    def calculate_for_resource(self, resources: Dict[str, float]):
        # Calcula el valor del indicador usando la fórmula y los recursos dados
        return ne.evaluate(self.formula, local_dict=resources)


class Evaluation(BaseModel):
    evaluation: Dict[str, float] = None

    def __init__(self, **data):
        super().__init__(**data)

    def to_list(self):
        return list(self.evaluation.values())

    def to_dataframe(self):
        return pd.DataFrame(self.evaluation, index=[0])


class Indicators(BaseModel):
    indicators: List[Indicator]
    single_evaluation: Evaluation = None
    evaluation_matrix: Dict[str, Evaluation] = {}
    multiple_alternatives: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        self._evaluation_result = None

    def add_indicator(self, indicator: Indicator):
        self.indicators.append(indicator)

    def evaluate_indicators(self, resources: Dict[str, float]):
        if resources.__class__ == list:
            self.multiple_alternatives = True
            for index, resource in enumerate(resources):
                evaluation_values = {}
                for indicator in self.indicators:
                    evaluation_values[indicator.name] = format(
                        indicator.calculate_for_resource(resource), f"{5}g"
                    )
                    self.evaluation_matrix[str(index)] = evaluation_values

        elif resources.__class__ == dict:
            self.multiple_alternatives = False
            evaluation_values = {}
            for indicator in self.indicators:
                evaluation_values[indicator.name] = format(
                    indicator.calculate_for_resource(resources), f"{5}g"
                )
                self.single_evaluation = Evaluation(evaluation=evaluation_values)
        else:
            raise ValueError("Resources must be a dictionary or a list")

    @property
    def len_indicators(self):
        return len(self.indicators)

    @property
    def evaluation(self):
        if self._evaluation_result is None:
            if self.multiple_alternatives:
                self._evaluation_result = pd.DataFrame.from_dict(
                    self.evaluation_matrix, orient="index"
                ).apply(pd.to_numeric)
            else:
                self._evaluation_result = self.single_evaluation
        return self._evaluation_result
