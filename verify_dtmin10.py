"""
Manual cross-check of HYSYS spreadsheet results for Delta Tmin = 10 degC
User-provided values from HYSYS:
  Total CAPEX          = 3.678e7  EUR
  Total Annual OPEX    = 8.624e6  EUR/yr
  CO2 produced         = 376,229.4 t/yr
  HOC                  = 3.864 MJ/kg CO2
  E-100 HX Area        = 2748 m2
"""

C1_SS_2021_EUR          = 1662000.0
A1_M2                   = 2747.0
EXPONENT_E              = 1.0
SS_TO_CS_FACTOR         = 1.75
HEX_AREA_REF_COST_2021  = C1_SS_2021_EUR / SS_TO_CS_FACTOR
INSTALL_FACTOR_E100     = 5.3
CEPCI_2026              = 830.0
CEPCI_2021              = 776.9
CEPCI_RATIO             = CEPCI_2026 / CEPCI_2021
OPERATING_HOURS         = 8000.0
STEAM_EUR_PER_KWH       = 0.015
ELECTRICITY_EUR_PER_KWH = 0.05
AF                      = 11.15
MAINTENANCE_FRAC        = 0.05
MEA_EUR_PER_YEAR        = 708571.0
ABSORBER_PURCHASE_2021  = 2994285.0
ABSORBER_IF             = 3.620
DESORBER_PURCHASE_2021  = 4385258.0
DESORBER_IF             = 3.330
CONDENSER_IF            = 9.480;  CONDENSER_U = 1.0;  CONDENSER_LMTD = 71.14
REBOILER_IF             = 5.30;   REBOILER_U  = 1.2;  REBOILER_LMTD  = 27.18
COOLER_IF               = 5.30;   COOLER_U    = 0.8;  COOLER_LMTD    = 27.0
E100_IF                 = 5.30;   E100_U      = 1.5

total_capex_user     = 3.678e7
total_opex_user      = 8.624e6
co2_tpy              = 376229.4
hoc_mj_per_kg        = 3.864
e100_area_m2         = 2748.0

co2_kgph         = co2_tpy * 1000.0 / OPERATING_HOURS
Q_reb_kJph       = hoc_mj_per_kg * 1000.0 * co2_kgph
Q_reb_kW         = Q_reb_kJph / 3600.0

print("=" * 65)
print("  CROSS-CHECK: HYSYS Spreadsheet vs Python Script Formulas")
print("  Delta Tmin = 10 degC")
print("=" * 65)

def area_based_cs_purchase_2021(area_m2):
    return HEX_AREA_REF_COST_2021 * ((area_m2 / A1_M2) ** EXPONENT_E)

def installed_2026(purchase_2021, install_factor):
    return purchase_2021 * install_factor * CEPCI_RATIO

C2_SS = C1_SS_2021_EUR * (e100_area_m2 / A1_M2)
C2_CS = C2_SS / SS_TO_CS_FACTOR
e100_capex = C2_CS * INSTALL_FACTOR_E100 * CEPCI_RATIO

reb_area = Q_reb_kW / (REBOILER_U * REBOILER_LMTD)
reb_purchase = area_based_cs_purchase_2021(reb_area)
reb_capex    = installed_2026(reb_purchase, REBOILER_IF)
abs_capex  = installed_2026(ABSORBER_PURCHASE_2021, ABSORBER_IF)
des_capex  = installed_2026(DESORBER_PURCHASE_2021, DESORBER_IF)

known_capex = e100_capex + reb_capex + abs_capex + des_capex
reboiler_opex = Q_reb_kW * OPERATING_HOURS * STEAM_EUR_PER_KWH
maintenance   = MAINTENANCE_FRAC * total_capex_user
ann_capex     = total_capex_user / AF
total_annual_cost = ann_capex + total_opex_user
capture_cost = total_annual_cost / co2_tpy

print(f"\nCAPTURE COST = {capture_cost:.3f} EUR/tCO2")
print(f"E-100 CAPEX  = {e100_capex:,.0f} EUR")
print(f"Reboiler CAPEX = {reb_capex:,.0f} EUR")
print("=" * 65)
