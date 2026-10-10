from itertools import product
from typing import List, Dict, Any
import numpy as np
import pandas as pd
from pydantic import BaseModel, validator
from .enums import ResourceEnum


class Alternatives(BaseModel):
    """
    Represents a set of alternatives generated based on resources and seed values.

    :param resources_included: A dictionary mapping ResourceEnum to a boolean value indicating whether the resource is included.
    :type resources_included: Dict[ResourceEnum, bool]
    :param seed: A list of seed values used for generating alternatives.
    :type seed: List[float]
    """

    resources_included: Dict[ResourceEnum, bool]
    seed: List[float]
    result: Any = None

    @validator("resources_included")
    def validate_resources_included(cls, v):
        """
        The validate_resources_included function is a validator that ensures all resources are of type ResourceEnum.
            It takes in the class and value as parameters, and returns the value if it passes validation.
            If not, it raises a ValueError.

        :param cls: Pass the class of the object being created
        :param v: Pass the value of the resources_included parameter
        :return: A dictionary of resources
        """
        if not all(isinstance(item, ResourceEnum) for item in v.keys()):
            raise ValueError("All resources must be of type ResourceEnum")
        if not v:
            raise ValueError("At least one resource must be configured")
        if not all(isinstance(item, bool) for item in v.values()):
            raise ValueError("Resource inclusion values must be boolean")
        return v

    @validator("seed")
    def validate_seed(cls, v):
        """
        The validate_seed function is a custom validator that ensures all seed values are of type float.
            It takes two arguments: the class and the value to be validated.
            The function first checks if all items in the list are floats, and raises an error if not.
            If they are, it returns them.

        :param cls: Pass the class to which the function belongs
        :param v: Pass the value of the seed attribute to the function
        :return: A list of floats
        :doc-author: Trelent
        """
        if not v:
            raise ValueError("At least one seed value must be configured")
        if not all(isinstance(item, (float, int)) for item in v):
            raise ValueError("All seed values must be numeric")
        if not all(np.isfinite(item) for item in v):
            raise ValueError("Seed values must be finite")
        return v

    def __init__(self, resources_included=None, seed=None):
        super().__init__(resources_included=resources_included, seed=seed)
        self.result = self.generate_alternatives()

    def generate_alternatives(self):
        """
        Generates a set of alternatives based on the resources and seed values.

        :return: A pandas DataFrame representing the generated alternatives.
        :rtype: pd.DataFrame
        """
        all_combinations = list(product(*[self.seed] * len(self.resources_included)))

        weight_scenarios = np.array(all_combinations)
        y_resources = np.array(list(self.resources_included.values()))

        scenario_matrix = weight_scenarios * y_resources
        scenario_array = list()
        for items in scenario_matrix:
            if np.isclose(sum(items), 1.0):
                scenario_array.append(list(items))

        scenario_array = list(
            dict.fromkeys(tuple(items) for items in scenario_array)
        )

        alternatives_df = pd.DataFrame(
            columns=[resource.value for resource in self.resources_included],
            data=scenario_array,
        )
        return alternatives_df

    @property
    def result_dict(self):
        """
        Returns the generated alternatives as a dictionary.

        :return: A dictionary representing the generated alternatives.
        :rtype: dict
        """
        return self.result.to_dict()

    @property
    def result_dataframe(self):
        """
        Returns the generated alternatives as a pandas DataFrame.

        :return: A pandas DataFrame representing the generated alternatives.
        :rtype: pd.DataFrame
        """
        return self.result
