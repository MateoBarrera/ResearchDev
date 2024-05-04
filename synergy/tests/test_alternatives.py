from synergy.alternative import Alternatives, ResourceEnum


def test_generate_alternatives():
    # Crear una instancia de Alternatives con recursos y semillas específicas
    resources_included = {
        ResourceEnum.SOLAR: True,
        ResourceEnum.WIND: True,
        ResourceEnum.HYDRO: True,
        ResourceEnum.BIOMASS: True,
    }

    alternatives = Alternatives(
        resources_included=resources_included, seed=[1, 0.5, 0.25, 0]
    )

    # Generar las alternativas
    alternatives_df = alternatives.result_dataframe
    # Verificar que el DataFrame de alternativas tiene la forma correcta
    assert alternatives_df.shape == (23, 4)

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
    assert all(value in alternatives.seed for value in alternatives_df.values.flatten())
