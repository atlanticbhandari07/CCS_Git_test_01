import win32com.client as win32
import sys

def diag():
    try:
        print("Connecting to HYSYS...")
        hysys = win32.Dispatch("HYSYS.Application")
        case = hysys.SimulationCases.Item(0)
        stream = case.Flowsheet.MaterialStreams.Item("CO2 product")
        print(f"Stream: {stream.name}")
        total_kgph = stream.MassFlow.GetValue("kg/h")
        print(f"Total Mass Flow (kg/h): {total_kgph}")
        total_internal = stream.MassFlowValue
        print(f"Total Mass Flow (internal): {total_internal}")
        ratio = total_kgph / total_internal if total_internal != 0 else 0
        print(f"Ratio (kg/h / internal): {ratio}")
        fractions = stream.ComponentMassFractionValue
        co2_frac = fractions[1]
        print(f"CO2 Mass Fraction: {co2_frac}")
        calculated_co2_kgph = total_kgph * co2_frac
        print(f"Calculated CO2 Mass Flow (kg/h): {calculated_co2_kgph}")
    except Exception as e:
        print(f"Diagnostic failed: {e}")

if __name__ == "__main__":
    diag()
