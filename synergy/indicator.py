import pandas as pd
from pydantic import BaseModel
from typing import Dict, List
from .enums import ResourceEnum, DimensionEnum
import numexpr as ne


class Indicator(BaseModel):
    """
    The Indicator class represents an indicator with various attributes such as id, name, dimension, description, source, data, year, unit, type_indicator, and formula.
    It provides methods to calculate the value of the formula based on the given resources.

    :param id: The unique identifier of the indicator.
    :param name: The name of the indicator.
    :param dimension: The dimension of the indicator.
    :param description: The description of the indicator.
    :param source: The source of the indicator.
    :param data: A dictionary that maps resource types to their corresponding values.
    :param year: The year of the indicator.
    :param unit: The unit of measurement for the indicator.
    :param type_indicator: The type of the indicator.
    :param formula: The formula used to calculate the indicator value.

    :ivar id: The unique identifier of the indicator.
    :ivar name: The name of the indicator.
    :ivar dimension: The dimension of the indicator.
    :ivar description: The description of the indicator.
    :ivar source: The source of the indicator.
    :ivar data: A dictionary that maps resource types to their corresponding values.
    :ivar year: The year of the indicator.
    :ivar unit: The unit of measurement for the indicator.
    :ivar type_indicator: The type of the indicator.
    :ivar formula: The formula used to calculate the indicator value.
    """

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

    def calculate_for_resource(self, resources: Dict[str, float]) -> float:
        """
        The calculate_for_resource function takes a dictionary of resources and returns the value of the formula.
        The function uses numexpr to evaluate the formula, which is much faster than using eval().

        :param resources: A dictionary of resources and their corresponding values.
        :type resources: Dict[str, float]
        :return: The result of the formula calculation.
        :rtype: float
        :raises: None
        """
        return ne.evaluate(self.formula, local_dict=resources)


class Evaluation(BaseModel):
    """
    Represents an evaluation object.

    :param evaluation: A dictionary containing the evaluation values.
    :type evaluation: Dict[str, float]
    """

    evaluation: Dict[str, float] = None

    def __init__(self, **data):
        super().__init__(**data)

    def to_list(self):
        """
        Converts the evaluation values to a list.

        Returns:
            list: A list containing the evaluation values.
        """
        return list(self.evaluation.values())

    def to_dataframe(self):
        """
        Converts the evaluation values to a pandas DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame containing the evaluation values.
        """
        return pd.DataFrame(self.evaluation, index=[0])


class Indicators(BaseModel):
    """
    Represents a collection of indicators.

    :param indicators: The list of indicators.
    :type indicators: List[Indicator]
    :param single_evaluation: The evaluation result when there is a single alternative.
    :type single_evaluation: Evaluation, optional
    :param evaluation_matrix: The evaluation results for multiple alternatives.
    :type evaluation_matrix: Dict[str, Evaluation], optional
    :param multiple_alternatives: Indicates whether there are multiple alternatives.
    :type multiple_alternatives: bool, optional

    **Methods**:

    __init__(self, **data)
        Initializes a new instance of the Indicators class.

    add_indicator(self, indicator: Indicator)
        Adds an indicator to the collection.

    evaluate_indicators(self, resources: Dict[str, float])
        Evaluates the indicators using the given resources.

    len_indicators(self)
        Returns the number of indicators in the collection.

    evaluation(self)
        Returns the evaluation result of the indicators.
    """

    indicators: List[Indicator]
    single_evaluation: Evaluation = None
    evaluation_matrix: Dict[str, Evaluation] = {}
    multiple_alternatives: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        self._evaluation_result = None

    def add_indicator(self, indicator: Indicator):
        """
        Adds an indicator to the collection.

        :param indicator: The indicator to be added.
        :type indicator: Indicator
        """
        self.indicators.append(indicator)

    def evaluate_indicators(self, resources: Dict[str, float]):
        """
        Evaluates the indicators using the given resources.

        :param resources: The resources used in the evaluation.
        :type resources: Dict[str, float]

        :raises ValueError: If the resources are not a dictionary or a list.
        """
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
        """
        Returns the number of indicators in the collection.

        :return: The number of indicators.
        :rtype: int
        """
        return len(self.indicators)

    @property
    def evaluation(self):
        """
        Returns the evaluation result of the indicators.

        If the evaluation result is not yet computed, it will be computed based on the evaluation matrix
        or the single evaluation, depending on whether there are multiple alternatives or not.

        :return: The evaluation result.
        :rtype: pandas.DataFrame or float
        """
        if self._evaluation_result is None:
            if self.multiple_alternatives:
                self._evaluation_result = pd.DataFrame.from_dict(
                    self.evaluation_matrix, orient="index"
                ).apply(pd.to_numeric)
            else:
                self._evaluation_result = self.single_evaluation
        return self._evaluation_result
