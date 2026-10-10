import json
from pathlib import Path

from compare_cases import compare_cases


def test_compare_cases_marks_different_runs_as_not_comparable(tmp_path):
    root = tmp_path
    for case_name, alternative_count, seed in (
        ("one", 10, [1.0, 0.5, 0.0]),
        ("two", 20, [1.0, 0.25, 0.0]),
    ):
        result_dir = root / "case_studies" / case_name / "results"
        result_dir.mkdir(parents=True)
        sensitivity_path = result_dir / "sensitivity.xlsx"
        import pandas as pd

        stability = pd.DataFrame({"mean_rank": [1.0], "rank_std": [0.0]})
        with pd.ExcelWriter(sensitivity_path) as writer:
            stability.to_excel(writer, sheet_name="rank_stability")
        manifest = {
            "created_at_utc": "2026-01-01T00:00:00+00:00",
            "alternative_count": alternative_count,
            "seed": seed,
            "topsis_scenario_count": 29,
            "hashes": {
                "code_sha256": "code",
                "weights_sha256": "weights",
            },
            "robust_alternative": {
                "alternative": "0",
                "top_5_rate": 1.0,
                "mean_rank": 1.0,
                "rank_std": 0.0,
                "best_rank": 1,
                "worst_rank": 1,
            },
            "outputs": {"sensitivity": str(sensitivity_path)},
        }
        (result_dir / "run_manifest.json").write_text(json.dumps(manifest))

    report, comparable = compare_cases(root, ["one", "two"])

    assert not comparable
    assert report["comparable_run"].eq(False).all()
