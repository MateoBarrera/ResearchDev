from pathlib import Path

import pytest

from synergy.validation import validate_case, validate_case_config


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    "case_name",
    ["jamundi", "santa_rosalia"],
)
def test_case_definitions_are_valid(case_name):
    config_path = PROJECT_ROOT / "case_studies" / case_name / "definition.yaml"

    config = validate_case(config_path, PROJECT_ROOT)

    assert config["CASE_STUDY"] == case_name


def test_validation_rejects_unknown_formula_variable(tmp_path):
    config = {
        "CASE_STUDY": "test",
        "INSTALLED_CAPACITY": 100,
        "RESOURCES": {
            "solar": {
                "name": "Solar",
                "file_name": "case_studies/jamundi/data/pv.csv",
            }
        },
    }
    indicators_path = tmp_path / "indicators.json"
    indicators_path.write_text(
        '[{"id": 1, "name": "Invalid", "dimension": "economic", '
        '"type_indicator": "cost", "formula": "unknown_variable + 1"}]',
        encoding="utf-8",
    )
    config["INDICATORS"] = str(indicators_path)

    with pytest.raises(ValueError):
        validate_case_config(config, PROJECT_ROOT)


def test_validation_rejects_unsorted_resource_data(tmp_path):
    resource_path = tmp_path / "solar.csv"
    resource_path.write_text(
        "YEAR,MO,DY,ALLSKY_SFC_SW_DWN\n"
        "2021,2,1,3.0\n"
        "2021,1,1,2.0\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="timestamps are not sorted"):
        from synergy.validation import _validate_resource_data

        _validate_resource_data("solar", resource_path)
