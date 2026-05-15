"""
Utility Functions Module
Provides helper functions for heat exchanger optimization.

This module includes:
- LMTD calculations with correction factors
- Temperature unit conversions
- Economic calculations (NPV, annualization)
- Data validation functions
"""

import logging
import math
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


def celsius_to_kelvin(temp_c: float) -> float:
    """Convert Celsius to Kelvin"""
    return temp_c + 273.15


def kelvin_to_celsius(temp_k: float) -> float:
    """Convert Kelvin to Celsius"""
    return temp_k - 273.15


def fahrenheit_to_celsius(temp_f: float) -> float:
    """Convert Fahrenheit to Celsius"""
    return (temp_f - 32) * 5/9


def celsius_to_fahrenheit(temp_c: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return temp_c * 9/5 + 32


def calculate_lmtd(T_h_in: float, T_h_out: float, T_c_in: float, T_c_out: float,
                   flow_config: str = 'counter-current') -> float:
    """
    Calculate Log Mean Temperature Difference (LMTD).

    Args:
        T_h_in: Hot stream inlet temperature (°C)
        T_h_out: Hot stream outlet temperature (°C)
        T_c_in: Cold stream inlet temperature (°C)
        T_c_out: Cold stream outlet temperature (°C)
        flow_config: 'counter-current' or 'co-current'

    Returns:
        LMTD in °C
    """
    if flow_config == 'counter-current':
        delta_T1 = T_h_in - T_c_out
        delta_T2 = T_h_out - T_c_in
    else:  # co-current
        delta_T1 = T_h_in - T_c_in
        delta_T2 = T_h_out - T_c_out

    if delta_T1 <= 0 or delta_T2 <= 0:
        logger.warning(f"Invalid temperature difference: ΔT1={delta_T1}, ΔT2={delta_T2}")
        return 0.0

    if abs(delta_T1 - delta_T2) < 0.01:
        lmtd = delta_T1
    else:
        lmtd = (delta_T1 - delta_T2) / math.log(delta_T1 / delta_T2)

    return lmtd


def calculate_lmtd_correction_factor(T_h_in: float, T_h_out: float,
                                     T_c_in: float, T_c_out: float,
                                     num_shell_passes: int = 1,
                                     num_tube_passes: int = 2) -> float:
    """
    Calculate LMTD correction factor (Ft) for shell-and-tube heat exchangers.
    For 1-shell pass, 2n-tube passes configuration.
    """
    P = (T_c_out - T_c_in) / (T_h_in - T_c_in)

    if abs(T_c_out - T_c_in) < 0.01:
        R = 0
    else:
        R = (T_h_in - T_h_out) / (T_c_out - T_c_in)

    if num_shell_passes == 1 and num_tube_passes == 1:
        return 1.0

    if num_shell_passes == 1 and num_tube_passes % 2 == 0:
        if abs(R - 1.0) < 0.01:
            Ft = (2/P - 1 - R) / ((2/P - 1 - R)**2 - R**2)**0.5 * math.log((1-P)/(1-P*R))
            Ft = Ft / math.log((2 - P*(R+1-(R**2+1)**0.5)) / (2 - P*(R+1+(R**2+1)**0.5)))
        else:
            S = (R**2 + 1)**0.5 / (R - 1)
            numerator = math.log((1 - P) / (1 - P*R))
            denominator = math.log((2/P - 1 - R + 2*S) / (2/P - 1 - R - 2*S))
            Ft = S * numerator / denominator

        Ft = max(0.5, min(1.0, Ft))
        return Ft

    logger.warning(f"Correction factor not implemented for {num_shell_passes}-{num_tube_passes} configuration")
    return 1.0


def calculate_npv(annual_cash_flow: float, discount_rate: float, years: int) -> float:
    """
    Calculate Net Present Value of annual cash flows.
    NPV = Σ(CF / (1 + r)^t) for t = 1 to n
    """
    npv = 0
    for year in range(1, years + 1):
        npv += annual_cash_flow / ((1 + discount_rate) ** year)
    return npv


def calculate_annualized_cost(total_cost: float, discount_rate: float, years: int) -> float:
    """
    Calculate annualized cost from total cost.
    Annualized Cost = Total Cost × [r(1+r)^n] / [(1+r)^n - 1]
    """
    if discount_rate == 0:
        return total_cost / years
    factor = (discount_rate * (1 + discount_rate)**years) / ((1 + discount_rate)**years - 1)
    return total_cost * factor


def calculate_total_cost(capex: float, opex_annual: float,
                         discount_rate: float = 0.10,
                         project_lifetime: int = 10) -> float:
    """
    Calculate total cost including CAPEX and NPV of OPEX.
    Total Cost = CAPEX + NPV(OPEX)
    """
    npv_opex = calculate_npv(-opex_annual, discount_rate, project_lifetime)
    total_cost = capex + abs(npv_opex)
    return total_cost


def validate_temperatures(T_h_in: float, T_h_out: float, T_c_in: float, T_c_out: float) -> Tuple[bool, str]:
    """
    Validate heat exchanger temperatures for physical feasibility.
    """
    if T_h_out >= T_h_in:
        return False, f"Hot stream must cool down: T_h_in={T_h_in}, T_h_out={T_h_out}"
    if T_c_out <= T_c_in:
        return False, f"Cold stream must heat up: T_c_in={T_c_in}, T_c_out={T_c_out}"
    if T_h_out <= T_c_in:
        return False, f"Temperature cross-over at cold end: T_h_out={T_h_out} <= T_c_in={T_c_in}"
    if T_h_in <= T_c_out:
        return False, f"Temperature cross-over at hot end: T_h_in={T_h_in} <= T_c_out={T_c_out}"
    return True, "Valid"


def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None):
    """Setup logging configuration."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    logger.info(f"Logging initialized at {log_level} level")


if __name__ == "__main__":
    lmtd = calculate_lmtd(150, 80, 30, 70, 'counter-current')
    print(f"LMTD: {lmtd:.2f}°C")
    npv = calculate_npv(-50000, 0.10, 10)
    print(f"NPV of $50,000/year for 10 years at 10%: ${abs(npv):,.2f}")
    total = calculate_total_cost(250000, 50000, 0.10, 10)
    print(f"Total cost (CAPEX + NPV OPEX): ${total:,.2f}")
    valid, msg = validate_temperatures(150, 80, 30, 70)
    print(f"Temperature validation: {valid} - {msg}")
