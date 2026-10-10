from __future__ import annotations

from typing import Iterable, Mapping

import numpy as np
import pandas as pd


def _normalize(matrix: np.ndarray) -> np.ndarray:
    norms = np.sqrt(np.sum(matrix**2, axis=0))
    normalized = np.zeros_like(matrix, dtype=float)
    nonzero = norms != 0
    normalized[:, nonzero] = matrix[:, nonzero] / norms[nonzero]
    return normalized


def _similarity_index(
    matrix: np.ndarray,
    weights: np.ndarray,
    type_indicators: Iterable[int],
) -> np.ndarray:
    type_indicators = list(type_indicators)
    if matrix.shape[1] != len(weights) or matrix.shape[1] != len(type_indicators):
        raise ValueError("Matrix, weights and criterion types must have equal width")
    if not all(item in (0, 1) for item in type_indicators):
        raise ValueError("Criterion types must be 0 (cost) or 1 (benefit)")
    weighted = _normalize(matrix) * weights
    ideal_positive = np.array(
        [
            column.max() if indicator == 1 else column.min()
            for column, indicator in zip(weighted.T, type_indicators)
        ]
    )
    ideal_negative = np.array(
        [
            column.min() if indicator == 1 else column.max()
            for column, indicator in zip(weighted.T, type_indicators)
        ]
    )
    positive_distance = np.linalg.norm(weighted - ideal_positive, axis=1)
    negative_distance = np.linalg.norm(weighted - ideal_negative, axis=1)
    denominator = positive_distance + negative_distance
    return np.divide(
        negative_distance,
        denominator,
        out=np.zeros_like(negative_distance),
        where=denominator != 0,
    )


def dimension_weight_scenarios(
    dimensions: Iterable[str],
) -> Mapping[str, dict[str, float]]:
    dimensions = list(dict.fromkeys(dimensions))
    if not dimensions:
        raise ValueError("At least one dimension is required")
    scenarios = {
        "balanced": {dimension: 1 / len(dimensions) for dimension in dimensions}
    }
    for dimension in dimensions:
        scenarios[f"emphasis_{dimension}"] = {
            name: 0.7 if name == dimension else 0.3 / (len(dimensions) - 1)
            for name in dimensions
        }
    return scenarios


def analyze_weight_sensitivity(
    indicator_matrix: pd.DataFrame,
    dimensions: Iterable[str],
    type_indicators: Iterable[int],
    alternatives: Iterable[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    dimensions = list(dimensions)
    if len(dimensions) != indicator_matrix.shape[1]:
        raise ValueError("Each indicator must have one dimension")
    if alternatives is None:
        alternatives = indicator_matrix.index.astype(str)
    alternatives = list(alternatives)
    if len(alternatives) != len(indicator_matrix):
        raise ValueError("Alternative labels must match the matrix rows")

    scenarios = dimension_weight_scenarios(dimensions)
    sensitivity = []
    for scenario_name, dimension_weights in scenarios.items():
        weights = np.array(
            [dimension_weights[dimension] / dimensions.count(dimension) for dimension in dimensions]
        )
        scores = _similarity_index(
            indicator_matrix.to_numpy(dtype=float),
            weights,
            type_indicators,
        )
        order = pd.Series(scores).rank(method="min", ascending=False).astype(int)
        for alternative, score, rank in zip(alternatives, scores, order):
            sensitivity.append(
                {
                    "scenario": scenario_name,
                    "alternative": alternative,
                    "similarity_index": score,
                    "rank": rank,
                }
            )

    result = pd.DataFrame(sensitivity)
    rank_pivot = result.pivot(index="alternative", columns="scenario", values="rank")
    scenario_names = list(scenarios)
    rank_pivot["mean_rank"] = rank_pivot[scenario_names].mean(axis=1)
    rank_pivot["rank_std"] = rank_pivot[scenario_names].std(axis=1, ddof=0)
    rank_pivot["best_rank"] = rank_pivot[scenario_names].min(axis=1)
    rank_pivot["worst_rank"] = rank_pivot[scenario_names].max(axis=1)
    rank_pivot["top_5_rate"] = (rank_pivot[scenario_names] <= 5).mean(axis=1)
    return result, rank_pivot.sort_values(["mean_rank", "rank_std"])


def select_robust_alternative(rank_stability: pd.DataFrame) -> dict:
    """Select the alternative with the strongest rank stability profile."""
    required_columns = {"top_5_rate", "rank_std", "mean_rank"}
    missing_columns = required_columns - set(rank_stability.columns)
    if missing_columns:
        raise ValueError(f"Missing stability columns: {sorted(missing_columns)}")
    selected = rank_stability.sort_values(
        ["top_5_rate", "rank_std", "mean_rank"],
        ascending=[False, True, True],
    ).iloc[0]
    return {
        "alternative": str(selected.name),
        "top_5_rate": float(selected["top_5_rate"]),
        "rank_std": float(selected["rank_std"]),
        "mean_rank": float(selected["mean_rank"]),
        "best_rank": int(selected["best_rank"]),
        "worst_rank": int(selected["worst_rank"]),
    }
