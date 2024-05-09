from synergy.resources import Solar, ResourceVariable
from synergy.alternative import Alternatives
from synergy.indicator import Indicators

INSTALLED_CAPACITY = 1000


solar = Solar(name="Solar PV Jamundí")
solar.add_variable(ResourceVariable(file_csv="data/pv/PV-Jamundi-H.csv"))
solar.evaluate(installed_capacity=INSTALLED_CAPACITY)
