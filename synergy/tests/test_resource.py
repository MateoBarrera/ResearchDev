from os import name
from synergy.resources.resource import ResourceVariable, Hydro, Solar, Wind
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


def test_resource_variable_from_excel():
    # Crear una instancia de ResourceVariable con datos específicos
    resource = ResourceVariable(file_excel="data/biomass/biomasa.xlsx")

    # Verificar que los atributos de la instancia son correctos
    assert resource.name == VariableEnum.BIOGAS
    assert resource.type_resource == ResourceType.BIOMASS
    assert resource.source == "ICA"
    assert resource.unit == Unit.CUBIT_METERS_PER_DAY
    assert resource.frequency == Frequency.MONTHLY


def test_hydro_resource():
    hydro = Hydro(name="Hydro Jamundi")
    hydro.add_variable(ResourceVariable(file_csv="data/hydro/Jamundi.min.csv"))
    result = hydro.evaluate(100)
    print(hydro.variability)
    assert result == 80, "Should be 80"
    assert hydro.variability == 52.96


def test_solar_resource():
    hydro = Solar(name="Solar Jamundi")
    hydro.add_variable(ResourceVariable(file_csv="data/pv/PV-Jamundi-H.csv"))
    result = hydro.evaluate(100)
    print(hydro.variability)
    assert result == 80, "Should be 80"
    assert hydro.variability == 52.96


def test_wind_resource():
    hydro = Wind(name="Wind Jamundi")
    hydro.add_variable(ResourceVariable(file_csv="data/wind/Wind-Jamundi-D-Nasa.csv"))
    result = hydro.evaluate(100)
    print(hydro.variability)
    assert result == 80, "Should be 80"
    assert hydro.variability == 52.96
