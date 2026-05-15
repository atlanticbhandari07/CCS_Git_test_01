"""
CAPEX (Capital Expenditure) Calculator Module
Calculates equipment and total installed cost for heat exchangers using
a simple base-cost scaling approach (six-tenths rule).

Formula:
    Equipment Cost = C1 × (A / A1) ^ n
    Total CAPEX = Equipment Cost × Installation Factor

Where:
    C1 = user-defined base (reference) equipment cost (EUR)
    A1 = reference area corresponding to C1 (m²)
    A  = calculated area for each Delta Tmin point (m²)
    n  = scaling exponent (default 0.6, six-tenths rule)
    Installation Factor = constant multiplier (default 5.30)
"""

import logging
import math
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CAPEXResult:
    """CAPEX calculation result"""
    area: float
    equipment_cost: float
    installation_factor: float
    total_capex: float
    base_cost_ref: float
    base_area_ref: float
    scaling_exponent: float

    def summary(self) -> str:
        """Generate summary string"""
        return f"""
CAPEX Breakdown
{'='*50}
Reference:  C1 = €{self.base_cost_ref:,.2f} at A1 = {self.base_area_ref:.2f} m²
Exponent:   n  = {self.scaling_exponent}
{'='*50}
Area:              {self.area:.2f} m²
Equipment Cost:    €{self.equipment_cost:,.2f}
Installation (×{self.installation_factor:.2f}): €{self.total_capex - self.equipment_cost:,.2f}
{'='*50}
TOTAL CAPEX:       €{self.total_capex:,.2f}
"""


class CAPEXCalculator:
    """
    Calculates capital expenditure for heat exchangers using simple
    base-cost scaling (six-tenths rule).

    CAPEX = C1 × (A / A1)^n × installation_factor
    """

    def __init__(self,
                 base_cost: float = 554000,
                 base_area: float = 2747,
                 scaling_exponent: float = 1,
                 installation_factor: float = 5.30):
        if base_cost <= 0:
            raise ValueError("base_cost must be positive")
        if base_area <= 0:
            raise ValueError("base_area must be positive")

        self.base_cost = base_cost
        self.base_area = base_area
        self.scaling_exponent = scaling_exponent
        self.installation_factor = installation_factor

        logger.info(f"CAPEX Calculator initialized: C1=€{base_cost:,.2f}, "
                    f"A1={base_area:.2f} m², n={scaling_exponent}, "
                    f"install_factor={installation_factor}")

    def calculate_equipment_cost(self, area: float) -> float:
        """Calculate scaled equipment cost for a given area. C = C1 × (A / A1) ^ n"""
        if area <= 0:
            raise ValueError("Area must be positive")
        equipment_cost = self.base_cost * (area / self.base_area) ** self.scaling_exponent
        logger.debug(f"Equipment cost for {area:.2f} m²: €{equipment_cost:,.2f}")
        return equipment_cost

    def calculate_capex(self, area: float) -> CAPEXResult:
        """Calculate total CAPEX for heat exchanger."""
        logger.info(f"Calculating CAPEX for area={area:.2f} m²")
        equipment_cost = self.calculate_equipment_cost(area)
        total_capex = equipment_cost * self.installation_factor
        result = CAPEXResult(
            area=area,
            equipment_cost=equipment_cost,
            installation_factor=self.installation_factor,
            total_capex=total_capex,
            base_cost_ref=self.base_cost,
            base_area_ref=self.base_area,
            scaling_exponent=self.scaling_exponent
        )
        logger.info(f"Total CAPEX: €{total_capex:,.2f}")
        return result

    def calculate_capex_simple(self, area: float) -> float:
        """Simplified CAPEX calculation returning only total cost."""
        return self.calculate_capex(area).total_capex


if __name__ == "__main__":
    calculator = CAPEXCalculator(
        base_cost=1662000,
        base_area=2747,
        scaling_exponent=1,
        installation_factor=5.30
    )
    areas = [50, 100, 150, 200, 250, 300]
    print("\nCAPEX vs Area Analysis")
    print("="*70)
    for area in areas:
        result = calculator.calculate_capex(area)
        print(f"{area:<15.1f} €{result.equipment_cost:>20,.2f}  €{result.total_capex:>20,.2f}")
    result = calculator.calculate_capex(area=150)
    print(result.summary())
