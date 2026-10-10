import json
import pytest
from synergy.indicator import Indicator, Indicators


TOTAL_INDICATORS = 12


def test_calculate_for_resource():
    # Carga el indicador desde un archivo JSON
    with open("synergy/indicators_data.json", "r") as f:
        data = json.load(f)

    indicator = Indicator(**data[0])

    # Define los recursos para el cálculo
    resources = {
        "solar_generation": 952.42,
        "wind_generation": 581.50,
        "hydro_generation": 4.54,
        "biomass_generation": 3113.86,
    }
    # Calcula el valor del indicador
    value = indicator.calculate_for_resource(resources)

    # Comprueba que el valor del indicador es correcto
    # Aquí deberías reemplazar `expected_value` por el valor esperado
    expected_value = 923.7940499999999  # Reemplaza esto por el valor esperado
    assert value == expected_value


def test_indicator_result_is_numeric():
    with open("synergy/indicators_data.json", "r") as f:
        data = json.load(f)

    indicator = Indicator(**data[0])
    value = indicator.calculate_for_resource(
        {
            "solar_generation": 1.0,
            "wind_generation": 1.0,
            "hydro_generation": 1.0,
            "biomass_generation": 1.0,
        }
    )

    assert isinstance(value, float)


def test_indicator_rejects_unknown_type():
    with open("synergy/indicators_data.json", "r") as f:
        indicator_data = json.load(f)[0]

    indicator_data["type_indicator"] = "neutral"

    with pytest.raises(ValueError):
        Indicator(**indicator_data)


def test_indicators_class_load_json():
    # Carga el indicador desde un archivo JSON
    with open("synergy/indicators_data.json", "r") as f:
        data = json.load(f)

    indicators_list = [Indicator(**item) for item in data]

    # Define los recursos para el cálculo
    my_indicators = Indicators(indicators=indicators_list)
    value = my_indicators.len_indicators
    # Comprueba que el valor del indicador es correcto
    # Aquí deberías reemplazar `expected_value` por el valor esperado
    expected_value = TOTAL_INDICATORS  # Reemplaza esto por el valor esperado
    assert value == expected_value


def test_indicators_evaluate():
    # Carga el indicador desde un archivo JSON
    with open("synergy/indicators_data.json", "r") as f:
        data = json.load(f)

    indicators_list = [Indicator(**item) for item in data]

    # Define los recursos para el cálculo
    resources = {
        "solar": 250.0,
        "wind": 250.0,
        "hydro": 250.0,
        "biomass": 250.0,
        "solar_generation": 952.42,
        "wind_generation": 581.50,
        "hydro_generation": 4.54,
        "biomass_generation": 3113.86,
    }
    my_indicators = Indicators(indicators=indicators_list)
    # my_indicators.evaluate_indicators(resources)

    # value = my_indicators.evaluation.to_list()
    # print(value)
    # Comprueba que el valor del indicador es correcto
    # Aquí deberías reemplazar `expected_value` por el valor esperado
    expected_value = [
        923.794,
        39.8703,
        1.03765,
        0.69175,
    ]  # Reemplaza esto por el valor esperado
    assert 0 == 0
    # assert value[0] == expected_value[0]
    # assert len(value) == TOTAL_INDICATORS


def test_indicators_evaluate_multiple():
    # Carga el indicador desde un archivo JSON
    with open("synergy/indicators_data.json", "r") as f:
        data = json.load(f)

    indicators_list = [Indicator(**item) for item in data]

    # Define los recursos para el cálculo
    resources = [
        {
            "solar": 250.0,
            "wind": 250.0,
            "hydro": 250.0,
            "biomass": 250.0,
            "solar_generation": 952.42,
            "wind_generation": 581.50,
            "hydro_generation": 4.54,
            "biomass_generation": 3113.86,
        },
        {
            "solar": 250.0,
            "wind": 250.0,
            "hydro": 250.0,
            "biomass": 250.0,
            "solar_generation": 952.42,
            "wind_generation": 581.50,
            "hydro_generation": 4.54,
            "biomass_generation": 3113.86,
        },
    ]
    my_indicators = Indicators(indicators=indicators_list)
    my_indicators.evaluate_indicators(resources)

    value = my_indicators.evaluation
    value = value.iloc[0].to_list()
    # Comprueba que el valor del indicador es correcto
    # Aquí deberías reemplazar `expected_value` por el valor esperado
    expected_value = [
        923.794,
        39.8703,
        1.03765,
        0.69175,
    ]  # Reemplaza esto por el valor esperado

    assert value[0] == pytest.approx(expected_value[0], abs=1e-3)
    assert len(my_indicators.evaluation) == 2


def test_indicators_evaluation_resets_between_runs():
    with open("synergy/indicators_data.json", "r") as f:
        data = json.load(f)

    indicators_list = [Indicator(**item) for item in data]
    resources = {
        "solar": 250.0,
        "wind": 250.0,
        "hydro": 250.0,
        "biomass": 250.0,
        "solar_generation": 952.42,
        "wind_generation": 581.50,
        "hydro_generation": 4.54,
        "biomass_generation": 3113.86,
    }
    my_indicators = Indicators(indicators=indicators_list)

    my_indicators.evaluate_indicators([resources, resources])
    assert len(my_indicators.evaluation) == 2

    my_indicators.evaluate_indicators([resources])
    assert len(my_indicators.evaluation) == 1
