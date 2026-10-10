from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd

from .console import console, pipeline_progress, show_run_header
from .enums import ResourceEnum
from .alternative import Alternatives
from .evaluation.mcda import Topsis
from .evaluation.mcda.sensitivity import (
    analyze_weight_sensitivity,
    select_robust_alternative,
)
from .indicator import Indicator, Indicators
from .resources import Biomass, Hydro, ResourceVariable, Solar, Wind
from .validation import load_case_config, resolve_path, validate_case_config

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

HASHED_CODE_FILES = (
    "synergy/runner.py",
    "synergy/validation.py",
    "synergy/alternative.py",
    "synergy/indicator.py",
    "synergy/evaluation/mcda/topsis.py",
    "synergy/resources/resource.py",
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _code_hash(project_root: Path) -> str:
    digest = hashlib.sha256()
    for relative_path in HASHED_CODE_FILES:
        path = project_root / relative_path
        digest.update(relative_path.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _load_config(config_path: str | Path, project_root: Path) -> dict:
    config = load_case_config(config_path, project_root)
    return validate_case_config(config, project_root)


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
    spinner_name: str = "dots12",
) -> dict:
    """Run one configured case and return its generated data and metadata."""
    root = Path(project_root).resolve() if project_root else _project_root()
    config = _load_config(config_path, root)
    config_path = resolve_path(config_path, root)
    capacity = config["INSTALLED_CAPACITY"]
    biomass_requirements = config.get("BIOMASS_REQUIREMENTS", {})
    resources_config = config["RESOURCES"]
    resource_models = {}
    seed_values = list(seed) if seed is not None else DEFAULT_SEED
    show_run_header(config["CASE_STUDY"], capacity, len(seed_values))
    progress_context = pipeline_progress(spinner_name=spinner_name)
    progress = progress_context.__enter__()
    progress_task = progress.add_task("Validación y preparación", total=4 + len(resources_config))
    console.print("[bold cyan]▶ Configuración validada; preparando recursos[/bold cyan]")
    progress.update(progress_task, description="Configuración validada; preparando recursos")
    progress.refresh()

    for resource_name, resource_config in resources_config.items():
        console.print(
            f"[cyan]▶ Cargando y evaluando recurso:[/cyan] {resource_name}"
        )
        progress.update(
            progress_task,
            description=f"Cargando y evaluando recurso: {resource_name}",
        )
        progress.refresh()
        if resource_name not in RESOURCE_CLASSES:
            raise ValueError(f"Unsupported resource: {resource_name}")
        resource_models[resource_name] = _load_resource(
            resource_name, resource_config, capacity
        )
        if resource_name == "biomass":
            resource_models[resource_name].evaluate(
                capacity, biomass_requirements, show_logs=False
            )
        else:
            resource_models[resource_name].evaluate(capacity, show_logs=False)
        progress.advance(progress_task)
        progress.update(progress_task, description=f"Recurso evaluado: {resource_name}")

    resources_included = {
        ResourceEnum(resource_name): True for resource_name in resource_models
    }
    alternatives = Alternatives(
        resources_included=resources_included,
        seed=seed_values,
    )
    alternatives_df = alternatives.result_dataframe * capacity
    console.print(
        f"[cyan]▶ Alternativas generadas:[/cyan] {len(alternatives_df):,}; "
        "evaluando generaciones"
    )
    progress.advance(progress_task)
    progress.update(progress_task, description="Alternativas generadas; evaluando generaciones")
    progress.refresh()

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
    indicator_path = resolve_path(indicator_path, root)
    weights_path = root / "synergy/evaluation/mcda/weight_criteria.xlsx"
    with indicator_path.open("r", encoding="utf-8") as file:
        indicator_data = json.load(file)

    console.print(f"[cyan]▶ Cargando indicadores:[/cyan] {len(indicator_data)}")
    progress.update(
        progress_task,
        description=f"Cargando {len(indicator_data)} indicadores",
    )
    progress.refresh()
    indicators = [Indicator(**item) for item in indicator_data]
    type_indicators = [int(item.type_indicator == "benefit") for item in indicators]
    weight_scenarios = pd.read_excel(weights_path, header=None)
    if (
        len(weight_scenarios) > 1
        and list(weight_scenarios.iloc[0])
        == list(range(weight_scenarios.shape[1]))
    ):
        weight_scenarios = weight_scenarios.iloc[1:]
    topsis_scenario_count = len(weight_scenarios)
    indicator_model = Indicators(indicators=indicators)
    indicator_model.evaluate_indicators(alternatives_df.to_dict(orient="records"))
    indicator_dimensions = [indicator.dimension.value for indicator in indicators]
    console.print("[cyan]▶ Indicadores evaluados; calculando ranking TOPSIS[/cyan]")
    topsis_task = progress.add_task("TOPSIS: preparando escenarios", total=topsis_scenario_count)
    progress.advance(progress_task)
    progress.update(progress_task, description="Indicadores evaluados; calculando TOPSIS")
    progress.refresh()

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
        progress_callback=lambda completed, total: (
            progress.update(
                topsis_task,
                description=f"TOPSIS: escenario {completed}/{total}",
                completed=completed,
            ),
            progress.refresh(),
        ),
    )
    console.print("[cyan]▶ Ranking TOPSIS calculado; analizando sensibilidad[/cyan]")
    progress.update(progress_task, description="Analizando sensibilidad de pesos")
    progress.refresh()
    progress.advance(progress_task)
    progress.update(progress_task, description="Ranking TOPSIS calculado; analizando sensibilidad")
    progress.refresh()

    sensitivity_detail, sensitivity_summary = analyze_weight_sensitivity(
        indicator_model.evaluation,
        indicator_dimensions,
        type_indicators,
        alternatives=alternatives_df.index.astype(str),
    )
    sensitivity_path = output_dir / f"sensitivity_{alternative_count}_alternatives.xlsx"
    with pd.ExcelWriter(sensitivity_path, engine="openpyxl") as writer:
        sensitivity_detail.to_excel(writer, sheet_name="scenario_results", index=False)
        sensitivity_summary.to_excel(writer, sheet_name="rank_stability")
    robust_alternative = select_robust_alternative(sensitivity_summary)
    console.print("[cyan]▶ Sensibilidad calculada; exportando resultados[/cyan]")
    progress.update(progress_task, description="Exportando Excel y manifiesto")
    progress.refresh()
    robust_index = int(robust_alternative["alternative"])
    resource_mix = {
        resource_name: float(alternatives_df.loc[robust_index, resource_name])
        for resource_name in resource_models
    }
    robust_alternative["resource_mix_kw"] = resource_mix
    robust_alternative["resource_mix_percent"] = {
        resource_name: value / capacity * 100
        for resource_name, value in resource_mix.items()
    }
    progress.advance(progress_task)
    progress.update(progress_task, description="Sensibilidad calculada; exportando resultados")
    progress.refresh()

    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "case_study": case_study,
        "installed_capacity": capacity,
        "seed": seed_values,
        "alternative_count": alternative_count,
        "indicator_count": len(indicators),
        "topsis_scenario_count": topsis_scenario_count,
        "robust_alternative": robust_alternative,
        "hashes": {
            "config_sha256": _sha256_file(config_path),
            "indicators_sha256": _sha256_file(indicator_path),
            "weights_sha256": _sha256_file(weights_path),
            "code_sha256": _code_hash(root),
        },
        "outputs": {
            "alternatives": str(alternatives_path),
            "ranking": str(output_dir / f"{ranking_name}.xlsx"),
            "sensitivity": str(sensitivity_path),
        },
    }
    manifest_path = output_dir / "run_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    progress_context.__exit__(None, None, None)

    return {
        "case_study": case_study,
        "alternative_count": alternative_count,
        "alternatives_path": alternatives_path,
        "ranking_path": output_dir / f"{ranking_name}.xlsx",
        "manifest_path": manifest_path,
        "manifest": manifest,
        "sensitivity_path": sensitivity_path,
        "dataframe": alternatives_df,
    }
