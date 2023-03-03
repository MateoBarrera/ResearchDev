from Evaluation.Resource.load import *
from Evaluation.alternative import *
from Evaluation.Indicator.indicator import *
from Evaluation.MCDA.model import ahp as AHP


hydro_data = PrimaryResource(
    name="Caudal medio mensual", type_resource="hydro", source="Ideam", station=26057040
)
hydro_data.from_csv("data/hydro/caudal_medio_mensual/Jamundi.csv.csv")

solar_data = PrimaryResource(name="Irradiance", type_resource="pv", source="pw_nasa")
solar_data.from_csv("data/pv/PV-Jamundi-H.csv")

wind_data = PrimaryResource(name="Wind speed", type_resource="wind", source="pw_nasa")
wind_data.from_csv("data/wind/Wind-Jamundi-D-Nasa.csv")


hydro = ResourceViability()
hydro.evaluate_resource(hydro_data)
solar = ResourceViability()
solar.evaluate_resource(solar_data)
wind = ResourceViability()
wind.evaluate_resource(wind_data)


power = hydro.potential(installed_capacity=1000, show=True)
power = solar.potential(installed_capacity=1000, show=True)
power = wind.potential(installed_capacity=1000, show=True)


alternatives = Alternatives(
    resources_included=[1, 1, 1, 0], seed=[1, 0.75, 0.5, 0.25, 0]
)
df_alternatives = alternatives.get()
print(alternatives)

total_installed_capacity = 4000  # kW

alternatives_kw = df_alternatives.mul(total_installed_capacity)
print("\n")
# print(alternatives_kw)

solar_array = []
hydro_array = []
wind_array = []

for index, alternative in alternatives_kw.iterrows():
    solar_array.append(solar.potential(alternative["solar"]))
    hydro_array.append(hydro.potential(alternative["hydro"]))
    wind_array.append(wind.potential(alternative["wind"]))


alternatives_kw["solar_generation"] = solar_array
alternatives_kw["hydro_generation"] = hydro_array
alternatives_kw["wind_generation"] = wind_array
# print(alternatives_kw.to_markdown(floatfmt=".1f"))


indicators = Indicators()
indicators.load("Evaluation/Indicator/indicators.json")
alternative_matrix = indicators.evaluate_alternative(alternatives_kw)
AHP(
    alternative_matrix=alternative_matrix,
    show_criteria_matrix=False,
    show_expert_matrix=False,
)
