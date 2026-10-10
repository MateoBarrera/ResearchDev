import numpy as np
import pandas as pd

from synergy.evaluation.mcda.sensitivity import (
    analyze_weight_sensitivity,
    select_robust_alternative,
)


def test_weight_sensitivity_returns_stability_summary():
    matrix = pd.DataFrame(
        [[1.0, 10.0], [2.0, 5.0], [3.0, 1.0]],
        columns=["economic", "technical"],
    )

    detail, summary = analyze_weight_sensitivity(
        matrix,
        dimensions=["economic", "technical"],
        type_indicators=[0, 1],
        alternatives=["A", "B", "C"],
    )

    assert set(detail["scenario"]) == {
        "balanced",
        "emphasis_economic",
        "emphasis_technical",
    }
    assert len(detail) == 9
    assert list(summary.index) == ["A", "B", "C"] or len(summary) == 3
    assert np.isfinite(summary["rank_std"]).all()


def test_select_robust_alternative_prioritizes_top_five_rate():
    summary = pd.DataFrame(
        {
            "top_5_rate": [0.6, 1.0],
            "rank_std": [0.1, 2.0],
            "mean_rank": [1.0, 3.0],
            "best_rank": [1, 1],
            "worst_rank": [2, 8],
        },
        index=["A", "B"],
    )

    robust = select_robust_alternative(summary)

    assert robust["alternative"] == "B"
    assert robust["top_5_rate"] == 1.0