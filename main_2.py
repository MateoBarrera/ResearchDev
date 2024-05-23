import json
from synergy import alternative
from synergy.resources import Solar, Wind, Hydro, Biomass, ResourceVariable
from synergy.alternative import Alternatives
from synergy.indicator import Indicators, Indicator
from synergy.evaluation.mcda import Topsis

INSTALLED_CAPACITY = 1000
BIOMASS_RESOURCES = {
    "harvest": {
        "sugar cane": 100,
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
solar.evaluate(installed_capacity=INSTALLED_CAPACITY, show_logs=True)

wind = Wind(name="Wind Jamundí")
wind.add_variable(ResourceVariable(file_csv="data/wind/Wind-Jamundi-D-Nasa.csv"))
wind.evaluate(installed_capacity=INSTALLED_CAPACITY, show_logs=True)

hydro = Hydro(name="Hydro Jamundí")
hydro.add_variable(ResourceVariable(file_csv="data/hydro/Jamundi.min.csv"))
hydro.evaluate(installed_capacity=INSTALLED_CAPACITY, show_logs=True)

biomass = Biomass(name="Biomass Jamundí")
biomass.add_variables(file_excel="data/biomass/biomasa.xlsx")
biomass.evaluate(INSTALLED_CAPACITY, BIOMASS_RESOURCES, show_logs=True)


RESOURCES_INCLUDE = {
    "solar": True,
    "wind": True,
    "hydro": True,
    "biomass": True,
}

alternatives = Alternatives(
    resources_included=RESOURCES_INCLUDE, seed=[1, 0.5, 0.25, 0]
)

alternatives_df = alternatives.result_dataframe * INSTALLED_CAPACITY
# print(alternatives_df)

solar_array = []
hydro_array = []
wind_array = []
biomass_array = []

for index, alternative in alternatives_df.iterrows():
    solar_array.append(solar.evaluate(alternative["solar"]))
    hydro_array.append(hydro.evaluate(alternative["hydro"]))
    wind_array.append(wind.evaluate(alternative["wind"]))
    biomass_array.append(biomass.evaluate(alternative["biomass"], BIOMASS_RESOURCES))

alternatives_df["solar_generation"] = solar_array
alternatives_df["hydro_generation"] = hydro_array
alternatives_df["wind_generation"] = wind_array
alternatives_df["biomass_generation"] = biomass_array

# print(alternatives_df)

with open("synergy/indicators_data.json", "r") as f:
    data = json.load(f)

indicators_list = [Indicator(**item) for item in data]

my_indicators = Indicators(indicators=indicators_list)
my_indicators.evaluate_indicators(alternatives_df.to_dict(orient="records"))

# print(my_indicators.evaluation)

# Escoge datos de evaluación de prueba
# 0 - expertos
# 1 - Igual importancia
# 2 - Enfoque Ambiental
# 3 - Enfoque Económico
# 4 - Enfoque Técnico
test_criteria = 0
Topsis(
    alternative_matrix=my_indicators.evaluation,
    show_criteria_matrix=True,
    show_expert_matrix=False,
    test=test_criteria,
    fuzzy=True,
    save_as="TOPSIS",
    alt_info=alternatives_df,
)
