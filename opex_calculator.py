"""
OPEX (Operating Expenditure) Calculator Module
Calculates annual operating costs for heat exchangers.

This module provides:
- Utility cost calculations (heating and cooling)
- Pumping cost calculations
- Maintenance cost estimates
- Total annual OPEX
"""

import logging
from typing import Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class UtilityCosts:
    """Utility cost parameters"""
    steam_cost: float = 17.0       # EUR/GJ
    hot_oil_cost: float = 20.0     # EUR/GJ
    cooling_water_cost: float = 0.03  # EUR/m³
    electricity_cost: float = 0.08    # EUR/kWh


@dataclass
class OPEXResult:
    """OPEX calculation result"""
    heating_cost_annual: float
    cooling_cost_annual: float
    pumping_cost_annual: float
    maintenance_cost_annual: float
    total_opex_annual: float
    heat_duty: float
    operating_hours: float

    def summary(self) -> str:
        return f"""
OPEX Breakdown (Annual)
{'='*50}
Heat Duty: {self.heat_duty:.2f} kW
Operating Hours: {self.operating_hours:,.0f} hours/year
Heating Utility Cost: €{self.heating_cost_annual:,.2f}/year
Cooling Utility Cost: €{self.cooling_cost_annual:,.2f}/year
{'='*50}
TOTAL OPEX: €{self.total_opex_annual:,.2f}/year
"""


class OPEXCalculator:
    """Calculates operating expenditure for heat exchangers."""

    def __init__(self,
                 utility_costs: Optional[UtilityCosts] = None,
                 operating_hours: float = 8000,
                 maintenance_factor: float = 0.04):
        self.utility_costs = utility_costs or UtilityCosts()
        self.operating_hours = operating_hours
        self.maintenance_factor = maintenance_factor
        logger.info(f"OPEX Calculator initialized: {operating_hours} h/year, {maintenance_factor*100}% maintenance")

    def calculate_heating_cost(self, heat_duty_kw: float, utility_type: str = 'steam') -> float:
        """Calculate annual heating utility cost."""
        if heat_duty_kw <= 0:
            return 0.0
        energy_gj_per_year = heat_duty_kw * 0.0036 * self.operating_hours
        unit_cost = self.utility_costs.hot_oil_cost if utility_type == 'hot_oil' else self.utility_costs.steam_cost
        annual_cost = energy_gj_per_year * unit_cost
        logger.debug(f"Heating cost: {energy_gj_per_year:.2f} GJ/year × €{unit_cost}/GJ = €{annual_cost:,.2f}/year")
        return annual_cost

    def calculate_cooling_cost(self, heat_duty_kw: float, utility_type: str = 'cooling_water',
                               cooling_water_temp_rise: float = 10.0) -> float:
        """Calculate annual cooling utility cost."""
        if heat_duty_kw <= 0:
            return 0.0
        flow_rate_kg_s = heat_duty_kw / (4.18 * cooling_water_temp_rise)
        flow_rate_m3_year = (flow_rate_kg_s / 1000) * 3600 * self.operating_hours
        annual_cost = flow_rate_m3_year * self.utility_costs.cooling_water_cost
        return annual_cost

    def calculate_pumping_cost(self, pressure_drop_kpa: float, flow_rate_kg_h: float,
                               pump_efficiency: float = 0.75) -> float:
        """Pumping cost (disabled per user request)."""
        return 0.0

    def calculate_maintenance_cost(self, capex: float) -> float:
        """Maintenance cost (disabled per user request)."""
        return 0.0

    def calculate_opex(self,
                       heat_duty_kw: float,
                       is_heating: bool,
                       capex: float,
                       utility_type: str = 'steam_lp',
                       pressure_drop_kpa: float = 50.0,
                       flow_rate_kg_h: float = 10000.0) -> OPEXResult:
        """Calculate total annual OPEX."""
        logger.info(f"Calculating OPEX: Q={heat_duty_kw:.2f} kW, {'heating' if is_heating else 'cooling'}")
        if is_heating:
            heating_cost = self.calculate_heating_cost(heat_duty_kw, utility_type)
            cooling_cost = 0.0
        else:
            heating_cost = 0.0
            cooling_cost = self.calculate_cooling_cost(heat_duty_kw, utility_type)
        total_opex = heating_cost + cooling_cost
        result = OPEXResult(
            heating_cost_annual=heating_cost,
            cooling_cost_annual=cooling_cost,
            pumping_cost_annual=0.0,
            maintenance_cost_annual=0.0,
            total_opex_annual=total_opex,
            heat_duty=heat_duty_kw,
            operating_hours=self.operating_hours
        )
        logger.info(f"Total OPEX: €{total_opex:,.2f}/year")
        return result

    def calculate_opex_simple(self, heat_duty_kw: float, is_heating: bool, capex: float) -> float:
        """Simplified OPEX calculation returning only total cost."""
        return self.calculate_opex(heat_duty_kw, is_heating, capex).total_opex_annual


if __name__ == "__main__":
    calculator = OPEXCalculator(operating_hours=8000, maintenance_factor=0.03)
    heat_duty = 485
    capex = 250000
    result = calculator.calculate_opex(
        heat_duty_kw=heat_duty, is_heating=False, capex=capex,
        utility_type='cooling_water', pressure_drop_kpa=50, flow_rate_kg_h=15000
    )
    print(result.summary())
