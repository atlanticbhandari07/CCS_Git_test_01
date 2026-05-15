import win32com.client as win32
import os

HYSYS_CASE_PATH = r"d:\BUUU\New simulation with new CAPEX sheet base case with spreadsheet.hsc"

try:
    hysys = win32.Dispatch("HYSYS.Application")
    case = None
    for i in range(hysys.SimulationCases.Count):
        c = hysys.SimulationCases.Item(i)
        if c.Pathname.lower() == HYSYS_CASE_PATH.lower():
            case = c
            break
    if not case:
        case = hysys.SimulationCases.Open(HYSYS_CASE_PATH)

    flowsheet = case.Flowsheet
    ops = flowsheet.Operations
    streams = flowsheet.MaterialStreams
    energy_streams = flowsheet.EnergyStreams

    co2_stream = streams.Item("CO2 product")
    reb_energy = energy_streams.Item("Reboiler duty")

    def get_component_massflow_kgph(stream, comp_name="CO2"):
        fp = stream.FluidPackage
        comps = fp.Components
        comp_idx = -1
        for i in range(comps.Count):
            if comps.Item(i).name.upper() == comp_name.upper():
                comp_idx = i
                break
        cmf_tuple = stream.ComponentMassFlowValue
        internal_rate = float(cmf_tuple[comp_idx])
        return internal_rate * 3600.0

    def get_energy_kjph(energy_stream):
        v = getattr(energy_stream, "HeatFlow")
        return float(v.GetValue("kJ/h"))

    co2_kgph = get_component_massflow_kgph(co2_stream, "CO2")
    Q_reb_kjph = get_energy_kjph(reb_energy)
    print(f"CO2 mass flow: {co2_kgph} kg/h")
    print(f"Reboiler Duty: {Q_reb_kjph} kJ/h")
    hoc_mj_per_kg = (Q_reb_kjph / co2_kgph / 1000.0)
    print(f"HOC: {hoc_mj_per_kg} MJ/kg CO2")

except Exception as e:
    import traceback
    traceback.print_exc()
