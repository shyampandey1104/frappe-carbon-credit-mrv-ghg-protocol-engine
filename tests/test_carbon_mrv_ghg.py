import unittest
from carbon_mrv_ghg.engine import EmissionActivityRecord, GHGProtocolCarbonMRVEngine

class TestGHGProtocolCarbonMRVEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GHGProtocolCarbonMRVEngine(enterprise_id="TATA-STEEL-EXPORT-UNIT")

    def test_scope_emissions(self):
        rec = EmissionActivityRecord(
            activity_id="ACT-2026-001", facility_code="PLANT-JAMSHEDPUR",
            scope_category="SCOPE_2_ELECTRICITY", fuel_or_source="GRID_ELECTRICITY_KWH_IN",
            quantity=100000.0, emission_factor_kg_co2e=0.72
        )
        res = self.engine.record_activity_emission(rec)
        self.assertEqual(res["emissions_tco2e"], 72.0)

    def test_cbam_embedded_carbon(self):
        res = self.engine.compute_embedded_cbam_footprint(
            product_code="STEEL-HOT-ROLLED-COIL", production_tonnes=500.0,
            direct_scope1_tco2e=650.0, indirect_scope2_tco2e=250.0
        )
        self.assertEqual(res["total_embodied_emissions_tco2e"], 900.0)
        self.assertEqual(res["cbam_carbon_intensity_tco2e_per_tonne"], 1.8)

    def test_offset_retirement(self):
        res = self.engine.retire_verified_carbon_offsets("VERRA-VCS-991204-IND", 50.0)
        self.assertEqual(res["status"], "PERMANENTLY_RETIRED_ON_REGISTRY")
        self.assertEqual(res["cumulative_retired_tco2e"], 50.0)

if __name__ == "__main__":
    unittest.main()
