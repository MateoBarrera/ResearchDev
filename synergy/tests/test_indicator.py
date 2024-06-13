import json
from synergy.indicator import Indicator, Indicators


TOTAL_INDICATORS = 9


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
    my_indicators.evaluate_indicators(resources)

    value = my_indicators.evaluation.to_list()
    print(value)
    # Comprueba que el valor del indicador es correcto
    # Aquí deberías reemplazar `expected_value` por el valor esperado
    expected_value = [
        923.794,
        39.8703,
        1.03765,
        0.69175,
    ]  # Reemplaza esto por el valor esperado
    assert value[0] == expected_value[0]
    assert len(value) == TOTAL_INDICATORS


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

    assert value[0] == expected_value[0]
    assert len(my_indicators.evaluation) == 2
