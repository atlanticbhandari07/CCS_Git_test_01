import win32com.client as win32
import time

HYSYS_CASE_PATH = r"d:\BUUU\New simulation with new CAPEX sheet.hsc"
hysys = win32.Dispatch("HYSYS.Application")
case = hysys.SimulationCases.Open(HYSYS_CASE_PATH)
absorber = case.Flowsheet.Operations.Item("Absorber")
stages_coll = absorber.ColumnFlowsheet.ColumnStages

try:
    case.Solver.CanSolve = False
    print(f"Current Stages: {stages_coll.Count}")
    try:
        print("Attempting to Add() without arguments...")
        stages_coll.Add()
        print("Success!")
    except Exception as e:
        print(f"Failed Add(): {e}")
    try:
        print("Attempting to Add('Stage_19')...")
        stages_coll.Add("Stage_19")
        print("Success!")
    except Exception as e:
        print(f"Failed Add('Stage_19'): {e}")
finally:
    case.Solver.CanSolve = True
