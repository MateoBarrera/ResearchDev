from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def load_case_report(project_root: Path, case_name: str) -> dict:
    result_dir = project_root / "case_studies" / case_name / "results"
    manifest_path = result_dir / "run_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sensitivity_path = Path(manifest["outputs"]["sensitivity"])
    if not sensitivity_path.is_absolute():
        sensitivity_path = project_root / sensitivity_path
    stability = pd.read_excel(
        sensitivity_path, sheet_name="rank_stability", index_col=0
    )
    robust = manifest["robust_alternative"]
    return {
        "case_study": case_name,
        "created_at_utc": manifest["created_at_utc"],
        "alternative_count": manifest["alternative_count"],
        "seed": manifest["seed"],
        "topsis_scenario_count": manifest["topsis_scenario_count"],
        "code_sha256": manifest["hashes"]["code_sha256"],
        "weights_sha256": manifest["hashes"]["weights_sha256"],
        "robust_alternative": robust["alternative"],
        "top_5_rate": robust["top_5_rate"],
        "mean_rank": robust["mean_rank"],
        "rank_std": robust["rank_std"],
        "best_rank": robust["best_rank"],
        "worst_rank": robust["worst_rank"],
        "stability_rows": len(stability),
    }


def compare_cases(project_root: Path, cases: list[str]) -> tuple[pd.DataFrame, bool]:
    reports = [load_case_report(project_root, case) for case in cases]
    report = pd.DataFrame(reports)
    comparable = all(
        report[column].map(json.dumps).nunique() == 1
        if column == "seed"
        else report[column].nunique() == 1
        for column in (
            "seed",
            "alternative_count",
            "topsis_scenario_count",
            "code_sha256",
            "weights_sha256",
        )
    )
    report["comparable_run"] = comparable
    return report, comparable


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare reproducible case-study runs")
    parser.add_argument("--case", nargs="+", default=["jamundi", "santa_rosalia"])
    parser.add_argument("--output", type=Path, default=Path("case_comparison.xlsx"))
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    report, comparable = compare_cases(project_root, args.case)
    report.to_excel(args.output, index=False)
    print(report.to_string(index=False))
    print(f"Comparable runs: {'yes' if comparable else 'no'}")
    print(f"Report: {args.output.resolve()}")


if __name__ == "__main__":
    main()
