import numpy as np

from synergy.evaluation.mcda.criteria import Criteria


def test_get_weighting_array_does_not_mutate_criteria():
    criteria = Criteria()
    criteria.weight_criteria = {
        "weights": np.array([0.6, 0.4]),
        "Environmental": np.array([0.7, 0.3]),
        "Technical": np.array([0.2, 0.8]),
    }

    first = criteria.get_weighting_array()
    second = criteria.get_weighting_array()

    assert np.array_equal(first, second)
    assert "weights" in criteria.weight_criteria