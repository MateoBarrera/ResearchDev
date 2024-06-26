from evaluation.resource.load import *
from evaluation.alternative import *
from evaluation.Indicator.indicator import *
from evaluation.MCDA.model import ahp as AHP
from evaluation.MCDA.model import topsis as TOPSIS

hydro_data = PrimaryResource(
    name="Caudal medio mensual", type_resource="hydro", source="Ideam", station=26057040
)
hydro_data.from_csv("data/hydro/caudal_medio_mensual/Jamundi.csv")


solar_data = PrimaryResource(name="Irradiance", type_resource="pv", source="pw_nasa")
solar_data.from_csv("data/pv/PV-Jamundi-H.csv")

wind_data = PrimaryResource(name="Wind speed", type_resource="wind", source="pw_nasa")
wind_data.from_csv("data/wind/Wind-Jamundi-D-Nasa.csv")

biomass_data = PrimaryResource(name="Biogas", type_resource="biomass", source="Other")
biomass_data.from_excel("data/biomass/biomasa.xlsx")


hydro = ResourceViability()
hydro.evaluate_resource(hydro_data)
# hydro.graph_resource()

solar = ResourceViability()
solar.evaluate_resource(solar_data)
# solar.graph_resource()


wind = ResourceViability()
wind.evaluate_resource(wind_data)
# wind.graph_resource()


biomass = ResourceViability(biomass_scenario=0)
biomass.evaluate_resource(biomass_data)
# biomass.graph_resource()

capacity_target = 1000

hydro.potential(installed_capacity=capacity_target, show=True)
solar.potential(installed_capacity=capacity_target, show=True)
wind.potential(installed_capacity=capacity_target, show=True)
biomass.potential(installed_capacity=capacity_target, show=True)

total_installed_capacity = capacity_target  # kW

alternatives = Alternatives(
    resources_included=[1, 1, 1, 1],
    seed=[1, 0.5, 0.25, 0],
    installed_capacity=total_installed_capacity,
)
df_alternatives = alternatives.get()
# print(alternatives)
alternatives_kw = df_alternatives.mul(total_installed_capacity)
print("\n")
# print(alternatives_kw)

solar_array = []
hydro_array = []
wind_array = []
biomass_array = []

for index, alternative in alternatives_kw.iterrows():
    solar_array.append(solar.potential(alternative["solar"]))
    hydro_array.append(hydro.potential(alternative["hydro"]))
    wind_array.append(wind.potential(alternative["wind"]))
    biomass_array.append(biomass.potential(alternative["biomass"]))

alternatives_kw["solar_generation"] = solar_array
alternatives_kw["hydro_generation"] = hydro_array
alternatives_kw["wind_generation"] = wind_array
alternatives_kw["biomass_generation"] = biomass_array
print(alternatives_kw.to_markdown(floatfmt=".1f"))


indicators = Indicators()
indicators.load("evaluation/Indicator/indicators.json")
alternative_matrix = indicators.evaluate_alternative(alternatives_kw)
print(alternative_matrix.to_markdown(floatfmt=".1f"))
# Escoge datos de evaluación de prueba
# 0 - expertos
# 1 - Igual importancia
# 2 - Enfoque Ambiental
# 3 - Enfoque Económico
# 4 - Enfoque Técnico
test_criteria = 0

# AHP(
#     alternative_matrix=alternative_matrix,
#     show_criteria_matrix=False,
#     show_expert_matrix=False,
#     test=test_criteria,
#     fuzzy=True,
#     save_as="AHP",
#    alt_info=alternatives_kw
# )

# TOPSIS(
#    alternative_matrix=alternative_matrix,
#    show_criteria_matrix=True,
#    show_expert_matrix=False,
#    test=test_criteria,
#    fuzzy=True,
#    save_as="TOPSIS",
#    alt_info=alternatives_kw,
# )

# 0 - expertos; 1 - Igual importancia; 2 - Enfoque Ambiental; 3 - Enfoque Económico; 4 - Enfoque Técnico
