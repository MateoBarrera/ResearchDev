from unittest import TestCase


class TestBiomass(TestCase):
    def setUp(self) -> None:
        from evaluation.resource.load import PrimaryResource, ResourceViability
        biomass_data = PrimaryResource(name="Biogas", type_resource="biomass", source="Other")
        biomass_data.from_excel("../../../data/biomass/biomasa.xlsx")
        self.biomass = ResourceViability(biomass_scenario=0)
        self.biomass.evaluate_resource(biomass_data)

    def test_is_viability(self):
        self.assertIs(type(self.biomass.is_viability), bool)

    def test_variability(self):
        self.assertEqual(1, 1)

    def test_autonomy(self):
        self.assertEqual(1, 1)

    def test_all_graph(self):
        self.biomass.graph_resource()
        self.assertEqual(1, 1)

    def test_transform_data(self):
        self.assertEqual(1, 1)

    def test_calculate_autonomy(self):
        self.assertEqual(1, 1)

    def test_potential(self):
        self.assertEqual(1, 1)
