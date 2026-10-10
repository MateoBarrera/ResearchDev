from __future__ import annotations

import ast
import json
import math
from datetime import datetime
from pathlib import Path

import yaml

from .enums import DimensionEnum, ResourceEnum
from .resources.utils.csv_readers import load_csv, load_data, load_excel

SUPPORTED_RESOURCES = {item.value for item in ResourceEnum}
SUPPORTED_INDICATOR_TYPES = {"cost", "benefit"}
KNOWN_FORMULA_NAMES = {
    resource.value for resource in ResourceEnum
} | {f"{resource.value}_generation" for resource in ResourceEnum}


def resolve_path(path: str | Path, project_root: Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else project_root / candidate


def load_case_config(config_path: str | Path, project_root: Path) -> dict:
    path = resolve_path(config_path, project_root)
    if not path.is_file():
        raise FileNotFoundError(f"Case configuration not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    if not isinstance(config, dict):
        raise ValueError("Case configuration must contain a mapping")
    return config


def _formula_names(formula: str) -> set[str]:
    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError as error:
        raise ValueError(f"Invalid indicator formula: {formula}") from error
    return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}


def _validate_resource_data(resource_name: str, resource_path: Path) -> None:
    if resource_name == "biomass":
        loaded = load_excel(str(resource_path))
        data_sets = [item["data"] for item in loaded]
    elif resource_path.suffix == ".data":
        data_sets = [load_data(str(resource_path))["data"]]
    else:
        data_sets = [load_csv(str(resource_path))["data"]]

    for data in data_sets:
        if resource_name != "biomass":
            timestamps = []
            for key in data:
                try:
                    timestamps.append(datetime.fromisoformat(str(key)))
                except ValueError as error:
                    raise ValueError(
                        f"Invalid timestamp in resource data: {key}"
                    ) from error
            if timestamps != sorted(timestamps):
                raise ValueError(f"Resource timestamps are not sorted: {resource_path}")
        values = list(data.values())
        if not values:
            raise ValueError(f"Resource data is empty: {resource_path}")
        if not all(isinstance(value, (int, float)) and math.isfinite(value) for value in values):
            raise ValueError(f"Resource data contains non-finite values: {resource_path}")
        if any(value < 0 for value in values):
            raise ValueError(f"Resource data contains negative values: {resource_path}")


def validate_case_config(config: dict, project_root: Path) -> dict:
    required_keys = {"CASE_STUDY", "INSTALLED_CAPACITY", "RESOURCES"}
    missing_keys = required_keys - config.keys()
    if missing_keys:
        missing = ", ".join(sorted(missing_keys))
        raise ValueError(f"Missing configuration key(s): {missing}")

    capacity = config["INSTALLED_CAPACITY"]
    if not isinstance(capacity, (int, float)) or not math.isfinite(capacity) or capacity <= 0:
        raise ValueError("INSTALLED_CAPACITY must be a positive finite number")

    resources = config["RESOURCES"]
    if not isinstance(resources, dict) or not resources:
        raise ValueError("RESOURCES must contain at least one resource")

    unknown_resources = set(resources) - SUPPORTED_RESOURCES
    if unknown_resources:
        names = ", ".join(sorted(unknown_resources))
        raise ValueError(f"Unsupported resource(s): {names}")

    for resource_name, resource_config in resources.items():
        if not isinstance(resource_config, dict):
            raise ValueError(f"Configuration for {resource_name} must be a mapping")
        for key in ("name", "file_name"):
            if not resource_config.get(key):
                raise ValueError(f"Resource {resource_name} requires {key}")
        resource_path = resolve_path(resource_config["file_name"], project_root)
        if not resource_path.is_file():
            raise FileNotFoundError(
                f"Input file for {resource_name} not found: {resource_path}"
            )
        _validate_resource_data(resource_name, resource_path)

    indicator_path = resolve_path(
        config.get("INDICATORS", "synergy/indicators_data.json"), project_root
    )
    if not indicator_path.is_file():
        raise FileNotFoundError(f"Indicator file not found: {indicator_path}")
    with indicator_path.open("r", encoding="utf-8") as file:
        indicators = json.load(file)
    if not isinstance(indicators, list) or not indicators:
        raise ValueError("Indicator file must contain a non-empty list")

    indicator_ids = []
    indicator_names = []
    active_formula_names = {
        resource_name for resource_name in resources
    } | {f"{resource_name}_generation" for resource_name in resources}
    for indicator in indicators:
        for key in (
            "id",
            "name",
            "dimension",
            "description",
            "source",
            "year",
            "unit",
            "data",
            "type_indicator",
            "formula",
        ):
            if key not in indicator:
                raise ValueError(f"Indicator is missing required key: {key}")
        indicator_ids.append(indicator["id"])
        indicator_names.append(indicator["name"])
        if indicator["dimension"] not in {item.value for item in DimensionEnum}:
            raise ValueError(f"Unsupported indicator dimension: {indicator['dimension']}")
        if indicator["type_indicator"] not in SUPPORTED_INDICATOR_TYPES:
            raise ValueError(
                f"Unsupported indicator type: {indicator['type_indicator']}"
            )
        if not isinstance(indicator["data"], dict):
            raise ValueError(f"Indicator data must be a mapping: {indicator['name']}")
        missing_data = set(resources) - indicator["data"].keys()
        if missing_data:
            names = ", ".join(sorted(missing_data))
            raise ValueError(f"Indicator is missing resource data: {names}")
        data_values = [indicator["data"][name] for name in resources]
        if not all(
            isinstance(value, (int, float)) and math.isfinite(value)
            for value in data_values
        ):
            raise ValueError(f"Indicator data contains non-finite values: {indicator['name']}")
        unknown_names = _formula_names(indicator["formula"]) - active_formula_names
        if unknown_names:
            names = ", ".join(sorted(unknown_names))
            raise ValueError(f"Unknown variable(s) in indicator formula: {names}")

    if len(indicator_ids) != len(set(indicator_ids)):
        raise ValueError("Indicator ids must be unique")
    if len(indicator_names) != len(set(indicator_names)):
        raise ValueError("Indicator names must be unique")

    weights_path = project_root / "synergy/evaluation/mcda/weight_criteria.xlsx"
    if not weights_path.is_file():
        raise FileNotFoundError(f"TOPSIS weights file not found: {weights_path}")

    import pandas as pd

    weights = pd.read_excel(weights_path, header=None).apply(pd.to_numeric)
    if len(weights) > 1 and list(weights.iloc[0]) == list(range(weights.shape[1])):
        weights = weights.iloc[1:].reset_index(drop=True)
    weight_values = weights.to_numpy(dtype=float)
    if weights.empty or not all(math.isfinite(value) for value in weight_values.flat):
        raise ValueError("TOPSIS weights must be finite and non-empty")
    if (weights < 0).any().any():
        raise ValueError("TOPSIS weights cannot be negative")
    if weights.shape[1] != len(indicators):
        raise ValueError(
            "TOPSIS weight columns must match the number of indicators"
        )
    if not all(
        math.isclose(row_sum, 1.0, rel_tol=1e-9, abs_tol=1e-9)
        for row_sum in weights.sum(axis=1)
    ):
        raise ValueError("Each TOPSIS weight scenario must sum to one")

    return config


def validate_case(config_path: str | Path, project_root: str | Path) -> dict:
    root = Path(project_root).resolve()
    config = load_case_config(config_path, root)
    return validate_case_config(config, root)
