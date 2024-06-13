from os import name
from synergy.resources.resource import ResourceVariable, Hydro, Solar, Wind, Biomass
from synergy.resources.enums import ResourceType, Unit, Frequency, VariableEnum


def test_resource_variable():
    # Crear una instancia de ResourceVariable con datos específicos
    resource = ResourceVariable(
        name=VariableEnum.SOLAR_IRRADIANCE,
        type_resource=ResourceType.SOLAR,
        source="TestSource",
        unit=Unit.KW,
        frequency=Frequency.HOURLY,
        data={"2021-01-01": 100.0, "2021-01-02": 200.0},
    )

    # Verificar que los atributos de la instancia son correctos
    assert resource.name == VariableEnum.SOLAR_IRRADIANCE
    assert resource.type_resource == ResourceType.SOLAR
    assert resource.source == "TestSource"
    assert resource.unit == Unit.KW
    assert resource.frequency == Frequency.HOURLY
    assert resource.data == {"2021-01-01": 100.0, "2021-01-02": 200.0}


def test_resource_variable_from_csv():
    # Crear una instancia de ResourceVariable con datos específicos
    resource = ResourceVariable(file_csv="data/hydro/Jamundi.min.csv")

    # Verificar que los atributos de la instancia son correctos
    assert resource.name == VariableEnum.FLOW_RIVER
    assert resource.type_resource == ResourceType.HYDRO
    assert resource.source == "IDEAM"
    assert resource.unit == Unit.CUBIT_METERS_PER_SECOND
    assert resource.frequency == Frequency.MONTHLY


def test_resource_variable_from_csv():
    # Crear una instancia de ResourceVariable con datos específicos
    resource = ResourceVariable(file_csv="data/pv/PV-Jamundi-H.csv")

    # Verificar que los atributos de la instancia son correctos
    assert resource.name == VariableEnum.SOLAR_IRRADIANCE
    assert resource.type_resource == ResourceType.SOLAR
    assert resource.source == "NASA"
    assert resource.unit == Unit.IRRADIANCE
    assert resource.frequency == Frequency.DAILY


def test_resource_variable_from_csv_2():
    # Crear una instancia de ResourceVariable con datos específicos
    resource = ResourceVariable(file_csv="data/wind/Wind-Jamundi-D-Nasa.csv")
    print(resource.data)
    # Verificar que los atributos de la instancia son correctos
    assert resource.name == VariableEnum.WIND_SPEED
    assert resource.type_resource == ResourceType.WIND
    assert resource.source == "NASA"
    assert resource.unit == Unit.METER_PER_SECOND
    assert resource.frequency == Frequency.DAILY


""" def test_resource_variable_from_excel():
    # Crear una instancia de ResourceVariable con datos específicos
    resource = ResourceVariable(file_excel="data/biomass/biomasa.xlsx")

    # Verificar que los atributos de la instancia son correctos
    assert resource.name == VariableEnum.BIOGAS
    assert resource.type_resource == ResourceType.BIOMASS
    assert resource.source == "ICA"
    assert resource.unit == Unit.CUBIT_METERS_PER_DAY
    assert resource.frequency == Frequency.MONTHLY """


def test_hydro_resource():
    hydro = Hydro(name="Hydro Jamundi")
    hydro.add_variable(ResourceVariable(file_csv="data/hydro/Jamundi.min.csv"))
    result = hydro.evaluate(100)
    print(hydro.variability)
    assert result == 524048.46095700096 / (365 * 24), "Should be 80"
    assert hydro.variability == 0.5259766012998586


def test_solar_resource():
    solar = Solar(name="Solar Jamundi")
    solar.add_variable(ResourceVariable(file_csv="data/pv/PV-Jamundi-H.csv"))
    result = solar.evaluate(100)
    print(solar.variability)
    assert result == 132858.62099999998 / (365 * 24), "Should be 80"
    assert solar.variability == 0.1507157094867947


def test_wind_resource():
    wind = Wind(name="Wind Jamundi")
    wind.add_variable(ResourceVariable(file_csv="data/wind/Wind-Jamundi-D-Nasa.csv"))
    result = wind.evaluate(100)
    print(wind.variability)
    assert result == 64905.328704546744 / (365 * 24), "Should be 80"
    assert wind.variability == 0.24880257392911043


def test_biomass_resource():
    biomass_sources = {
        "harvest": {
            "sugar cane": 10,
            "rice": 2,
            "citrus": 3,
            "banana": 0,
            "coffee": 0,
            "pineapple": 0,
        },
        "livestock": {"cattle": 100},
    }
    biomass = Biomass(name="Biomass Jamundí")
    biomass.add_variables(file_excel="data/biomass/biomasa.xlsx")
    result = biomass.evaluate(1000, biomass_sources)
    assert biomass.name == "Biomass Jamundí"
    assert result == 14.00149755214819, "Should be 14.001497"
