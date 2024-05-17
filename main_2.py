from synergy.resources import Solar, Wind, Hydro, Biomass, ResourceVariable
from synergy.alternative import Alternatives
from synergy.indicator import Indicators

INSTALLED_CAPACITY = 1000
BIOMASS_RESOURCES = {
    "harvest": {
        "sugar cane": 10,
        "rice": 2,
        "citrus": 3,
        "banana": 0,
        "coffee": 5,
        "pineapple": 0,
    },
    "livestock": {"cattle": 150, "pig": 200, "poultry": 2000},
}


solar = Solar(name="Solar PV Jamundí")
solar.add_variable(ResourceVariable(file_csv="data/pv/PV-Jamundi-H.csv"))
solar.evaluate(installed_capacity=INSTALLED_CAPACITY)

wind = Wind(name="Wind Jamundí")
wind.add_variable(ResourceVariable(file_csv="data/wind/Wind-Jamundi-D-Nasa.csv"))
wind.evaluate(installed_capacity=INSTALLED_CAPACITY)

hydro = Hydro(name="Hydro Jamundí")
hydro.add_variable(ResourceVariable(file_csv="data/hydro/Jamundi.min.csv"))
hydro.evaluate(installed_capacity=INSTALLED_CAPACITY)

biomass = Biomass(name="Biomass Jamundí")
biomass.add_variables(file_excel="data/biomass/biomasa.xlsx")
biomass.evaluate(INSTALLED_CAPACITY, BIOMASS_RESOURCES)
