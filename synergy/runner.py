from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import yaml
from tqdm import tqdm

from .enums import ResourceEnum
from .alternative import Alternatives
from .evaluation.mcda import Topsis
from .indicator import Indicator, Indicators
from .resources import Biomass, Hydro, ResourceVariable, Solar, Wind

DEFAULT_SEED = [
    1.0,
    0.96,
    0.92,
    0.88,
    0.84,
    0.8,
    0.76,
    0.72,
    0.68,
    0.64,
    0.6,
    0.56,
    0.52,
    0.48,
    0.44,
    0.4,
    0.36,
    0.32,
    0.28,
    0.24,
    0.2,
    0.16,
    0.12,
    0.08,
    0.04,
    0.0,
]

RESOURCE_CLASSES = {
    "solar": Solar,
    "wind": Wind,
    "hydro": Hydro,
    "biomass": Biomass,
}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _resolve_path(path: str | Path, project_root: Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    return candidate


def _load_config(config_path: str | Path, project_root: Path) -> dict:
    path = _resolve_path(config_path, project_root)
    if not path.is_file():
        raise FileNotFoundError(f"Case configuration not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    if not isinstance(config, dict):
        raise ValueError("Case configuration must contain a mapping")
    for required_key in ("CASE_STUDY", "INSTALLED_CAPACITY", "RESOURCES"):
        if required_key not in config:
            raise ValueError(f"Missing configuration key: {required_key}")
    return config


def _load_resource(resource_name: str, resource_config: dict, capacity: float):
    resource_class = RESOURCE_CLASSES[resource_name]
    resource = resource_class(name=resource_config["name"])
    resource.add_variable(
        ResourceVariable(file_name=resource_config["file_name"])
    ) if resource_name != "biomass" else resource.add_variables(
        file_name=resource_config["file_name"]
    )
    return resource


def run_case(
    config_path: str | Path,
    seed: Iterable[float] | None = None,
    project_root: str | Path | None = None,
) -> dict:
    """Run one configured case and return its generated data and metadata."""
    root = Path(project_root).resolve() if project_root else _project_root()
    config = _load_config(config_path, root)
    capacity = config["INSTALLED_CAPACITY"]
    biomass_requirements = config.get("BIOMASS_REQUIREMENTS", {})
    resources_config = config["RESOURCES"]
    resource_models = {}

    for resource_name, resource_config in resources_config.items():
        if resource_name not in RESOURCE_CLASSES:
            raise ValueError(f"Unsupported resource: {resource_name}")
        resource_models[resource_name] = _load_resource(
            resource_name, resource_config, capacity
        )
        if resource_name == "biomass":
            resource_models[resource_name].evaluate(
                capacity, biomass_requirements, show_logs=True
            )
        else:
            resource_models[resource_name].evaluate(capacity, show_logs=True)

    resources_included = {
        ResourceEnum(resource_name): True for resource_name in resource_models
    }
    alternatives = Alternatives(
        resources_included=resources_included,
        seed=list(seed) if seed is not None else DEFAULT_SEED,
    )
    alternatives_df = alternatives.result_dataframe * capacity

    for resource_name, resource_model in resource_models.items():
        generation = []
        for _, alternative_row in alternatives_df.iterrows():
            resource_capacity = alternative_row[resource_name]
            if resource_name == "biomass":
                value = resource_model.evaluate(
                    resource_capacity, biomass_requirements
                )
            else:
                value = resource_model.evaluate(resource_capacity)
            generation.append(value)
        alternatives_df[f"{resource_name}_generation"] = generation

    indicator_path = config.get("INDICATORS", "synergy/indicators_data.json")
    indicator_path = _resolve_path(indicator_path, root)
    with indicator_path.open("r", encoding="utf-8") as file:
        indicator_data = json.load(file)

    indicators = [Indicator(**item) for item in tqdm(indicator_data, desc="Loading Indicators")]
    type_indicators = [int(item.type_indicator == "benefit") for item in indicators]
    indicator_model = Indicators(indicators=indicators)
    indicator_model.evaluate_indicators(alternatives_df.to_dict(orient="records"))

    case_study = config["CASE_STUDY"]
    output_dir = root / "case_studies" / case_study / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    alternative_count = alternatives_df.shape[0]
    alternatives_path = output_dir / f"alternatives_{alternative_count}.xlsx"
    ranking_name = f"ranking_of_{alternative_count}_alternatives"
    alternatives_df.to_excel(alternatives_path, engine="openpyxl")

    Topsis(
        alternative_matrix=indicator_model.evaluation,
        show_criteria_matrix=True,
        show_expert_matrix=False,
        test=-1,
        fuzzy=True,
        alt_info=alternatives_df,
        save_as=ranking_name,
        case_study=case_study,
        type_indicators=type_indicators,
    )

    return {
        "case_study": case_study,
        "alternative_count": alternative_count,
        "alternatives_path": alternatives_path,
        "ranking_path": output_dir / f"{ranking_name}.xlsx",
        "dataframe": alternatives_df,
    }
