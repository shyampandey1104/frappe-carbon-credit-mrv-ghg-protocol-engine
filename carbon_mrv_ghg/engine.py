"""GHG Protocol Corporate Standard (Scope 1, 2, 3) & EU CBAM Carbon MRV Engine."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class EmissionActivityRecord:
    activity_id: str
    facility_code: str
    scope_category: str  # SCOPE_1_DIRECT, SCOPE_2_ELECTRICITY, SCOPE_3_SUPPLY_CHAIN
    fuel_or_source: str  # DIESEL_LITRES, GRID_ELECTRICITY_KWH, AIR_FREIGHT_TON_KM
    quantity: float
    emission_factor_kg_co2e: float
    total_co2e_metric_tons: float = 0.0

class GHGProtocolCarbonMRVEngine:
    # Standard emission factors (kg CO2e per unit)
    DEFAULT_FACTORS = {
        "DIESEL_LITRES": 2.68,              # Scope 1
        "NATURAL_GAS_SCM": 1.95,            # Scope 1
        "GRID_ELECTRICITY_KWH_IN": 0.72,    # Scope 2 (CEA Indian grid factor)
        "GRID_ELECTRICITY_KWH_EU": 0.25,    # Scope 2 (EU residual mix)
        "ROAD_FREIGHT_TON_KM": 0.096,       # Scope 3
        "AIR_FREIGHT_TON_KM": 0.602         # Scope 3
    }

    def __init__(self, enterprise_id: str):
        self.enterprise_id = enterprise_id
        self.activities: Dict[str, EmissionActivityRecord] = {}
        self.retired_offsets_tco2e = 0.0

    def record_activity_emission(self, rec: EmissionActivityRecord) -> Dict[str, Any]:
        co2e_kg = round(rec.quantity * rec.emission_factor_kg_co2e, 2)
        rec.total_co2e_metric_tons = round(co2e_kg / 1000.0, 3)
        self.activities[rec.activity_id] = rec
        return {
            "activity_id": rec.activity_id,
            "scope": rec.scope_category,
            "emissions_tco2e": rec.total_co2e_metric_tons
        }

    def compute_embedded_cbam_footprint(self, product_code: str, production_tonnes: float, direct_scope1_tco2e: float, indirect_scope2_tco2e: float) -> Dict[str, Any]:
        if production_tonnes <= 0:
            raise ValueError("Production tonnes must be greater than zero.")
        total_embodied = direct_scope1_tco2e + indirect_scope2_tco2e
        intensity_per_tonne = round(total_embodied / production_tonnes, 4)
        return {
            "product_code": product_code,
            "production_volume_tonnes": production_tonnes,
            "direct_scope1_tco2e": direct_scope1_tco2e,
            "indirect_scope2_tco2e": indirect_scope2_tco2e,
            "total_embodied_emissions_tco2e": round(total_embodied, 3),
            "cbam_carbon_intensity_tco2e_per_tonne": intensity_per_tonne
        }

    def retire_verified_carbon_offsets(self, registry_serial_no: str, offset_tco2e: float) -> Dict[str, Any]:
        if offset_tco2e <= 0:
            raise ValueError("Retirement tonnes must be strictly positive.")
        self.retired_offsets_tco2e += offset_tco2e
        return {
            "registry_serial_no": registry_serial_no,
            "retired_tco2e": offset_tco2e,
            "cumulative_retired_tco2e": round(self.retired_offsets_tco2e, 3),
            "status": "PERMANENTLY_RETIRED_ON_REGISTRY"
        }
