import pytest
import numpy as np

from synergy.alternative import Alternatives, ResourceEnum


def test_generate_alternatives():
    # Crear una instancia de Alternatives con recursos y semillas específicas
    resources_included = {
        ResourceEnum.SOLAR: True, #Tech
        ResourceEnum.WIND: True, #Eco
        ResourceEnum.HYDRO: True, #Soc
        ResourceEnum.BIOMASS: False, 
    }

    alternatives = Alternatives(
        resources_included=resources_included, seed=[0.8, 0.6, 0.4, 0.2]
    )

    print("Alternatives seed:", alternatives.seed)
    print(alternatives.result_dataframe)
    # Generar las alternativas
    alternatives_df = alternatives.result_dataframe
    # Verificar que el DataFrame de alternativas tiene la forma correcta
    assert alternatives_df.shape == (6, 4)

    # Verificar que las columnas del DataFrame son correctas
    assert list(alternatives_df.columns) == [
        ResourceEnum.SOLAR.value,
        ResourceEnum.WIND.value,
        ResourceEnum.HYDRO.value,
        ResourceEnum.BIOMASS.value,
    ]

    # Verificar que las sumas de las filas del DataFrame son todas 1
    assert all(alternatives_df.sum(axis=1) == 1)

    # Verificar que todos los valores del DataFrame están en la semilla
    assert all(
        value == 0 or value in alternatives.seed
        for value in alternatives_df.values.flatten()
    )


def test_generate_alternatives_accepts_integer_seed_values():
    alternatives = Alternatives(
        resources_included={ResourceEnum.SOLAR: True, ResourceEnum.WIND: True},
        seed=[1, 0],
    )

    assert len(alternatives.result_dataframe) == 2
    assert np.allclose(alternatives.result_dataframe.sum(axis=1), 1.0)


def test_generate_alternatives_rejects_empty_resources():
    with pytest.raises(ValueError, match="At least one resource"):
        Alternatives(resources_included={}, seed=[1.0, 0.0])
