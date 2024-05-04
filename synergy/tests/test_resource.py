from synergy.resources.resource import ResourceVariable
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
    assert resource.unit == Unit.CUBIT_METER_PER_SECOND
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
