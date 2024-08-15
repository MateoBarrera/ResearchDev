import yaml
import json
from datetime import datetime
from synergy import alternative
from synergy.resources import Solar, Wind, Hydro, Biomass, ResourceVariable
from synergy.alternative import Alternatives
from synergy.indicator import Indicators, Indicator
from synergy.evaluation.mcda import Topsis

TODAY = datetime.now().strftime("%Y-%m-%d")

with open("case_studies/case_1.yaml", "r") as file:
    config = yaml.safe_load(file)

CASE_STUDY = config["CASE_STUDY"]
INSTALLED_CAPACITY = config["INSTALLED_CAPACITY"]
BIOMASS_REQUIREMENTS = config["BIOMASS_REQUIREMENTS"]
RESOURCES_INCLUDE = {}

RESOURCES_INCLUDE["solar"] = "solar" in config["RESOURCES"]
if RESOURCES_INCLUDE["solar"]:
    solar_config = config["RESOURCES"]["solar"]
    solar = Solar(name=solar_config["name"])
    solar.add_variable(ResourceVariable(file_name=solar_config["file_name"]))
    solar.evaluate(installed_capacity=INSTALLED_CAPACITY, show_logs=True)

RESOURCES_INCLUDE["wind"] = "wind" in config["RESOURCES"]
if RESOURCES_INCLUDE["wind"]:
    wind_config = config["RESOURCES"]["wind"]
    wind = Wind(name=wind_config["name"])
    wind.add_variable(ResourceVariable(file_name=wind_config["file_name"]))
    wind.evaluate(installed_capacity=INSTALLED_CAPACITY, show_logs=True)

RESOURCES_INCLUDE["hydro"] = "hydro" in config["RESOURCES"]
if RESOURCES_INCLUDE["hydro"]:
    hydro_config = config["RESOURCES"]["hydro"]
    hydro = Hydro(name=hydro_config["name"])
    hydro.add_variable(ResourceVariable(file_name=hydro_config["file_name"]))
    hydro.evaluate(installed_capacity=INSTALLED_CAPACITY, show_logs=True)

RESOURCES_INCLUDE["biomass"] = "biomass" in config["RESOURCES"]
if RESOURCES_INCLUDE["biomass"]:
    biomass_config = config["RESOURCES"]["biomass"]
    biomass = Biomass(name=biomass_config["name"])
    biomass.add_variables(file_name=biomass_config["file_name"])
    biomass.evaluate(INSTALLED_CAPACITY, BIOMASS_REQUIREMENTS, show_logs=True)


# TODO For seed in seeds loop

alternatives = Alternatives(
    resources_included=RESOURCES_INCLUDE,
    seed=[1, 0.5, 0.25, 0],
)

##
# seed=[1, 0.5, 0.25, 0]
# seed=[1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
# seed=[1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]
# seed=[1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.0]

alternatives_df = alternatives.result_dataframe * INSTALLED_CAPACITY
save_as_a = alternatives_df.shape[0]
# print(alternatives_df)

# ISSUE: The array initialization is not dynamic
solar_array = []
hydro_array = []
wind_array = []
biomass_array = []

for index, alternative in alternatives_df.iterrows():
    solar_array.append(solar.evaluate(alternative["solar"]))
    hydro_array.append(hydro.evaluate(alternative["hydro"]))
    wind_array.append(wind.evaluate(alternative["wind"]))
    biomass_array.append(biomass.evaluate(alternative["biomass"], BIOMASS_REQUIREMENTS))

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
print(my_indicators.evaluation.shape)

# Escoge datos de evaluación de prueba
# -1 - Automático
#  0 - expertos
#  1 - Igual importancia
#  2 - Enfoque Ambiental
#  3 - Enfoque Económico
#  4 - Enfoque Técnico
test_criteria = -1
Topsis(
    alternative_matrix=my_indicators.evaluation,
    show_criteria_matrix=True,
    show_expert_matrix=False,
    test=test_criteria,
    fuzzy=True,
    alt_info=alternatives_df,
    save_as=f"ranking_of_{save_as_a}_alternatives",
    case_study=CASE_STUDY,
)
