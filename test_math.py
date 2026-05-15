# test_math.py

co2_kgph = 100000.0  # 100 t/h
hoc_mj_per_kg = 3.866

Q_reb_kjph = hoc_mj_per_kg * co2_kgph * 1000.0  # kJ/h
print(f"Q_reb_kjph: {Q_reb_kjph} kJ/h")

OPERATING_HOURS_PER_YEAR = 8000.0
STEAM_PRICE_EUR_PER_KWH = 0.015

Q_reb_kw = Q_reb_kjph / 3600.0
annual_energy_kwh = Q_reb_kw * OPERATING_HOURS_PER_YEAR
reboiler_annual_opex = annual_energy_kwh * STEAM_PRICE_EUR_PER_KWH

print(f"Reboiler annual OPEX: {reboiler_annual_opex} EUR/y")

co2_tpy = (co2_kgph * OPERATING_HOURS_PER_YEAR) / 1000.0
print(f"CO2 t/y: {co2_tpy} t/y")

reboiler_opex_per_t = reboiler_annual_opex / co2_tpy
print(f"Reboiler OPEX per tCO2: {reboiler_opex_per_t} EUR/tCO2")
