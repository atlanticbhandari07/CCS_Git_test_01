"""
inspect_absorber_stages.py
---------------------------
Run this ONCE with HYSYS open and the simulation case loaded.
Prints every stage-related property/method on the absorber column object.
"""

import win32com.client as win32

HYSYS_CASE_PATH = r"d:\BUUU\New simulation with new CAPEX sheet.hsc"
ABSORBER_NAME   = "Absorber"

STAGE_KEYWORDS = {
    "stage", "tray", "pack", "height", "count", "number", "numb", "num",
    "section", "bed", "efficiency", "murphree"
}

def show_attrs(obj, label, depth=0, max_depth=3):
    if depth > max_depth:
        return
    indent = "  " * depth
    print(f"\n{indent}=== {label} ===")
    try:
        attrs = [a for a in dir(obj) if not a.startswith("_")]
    except Exception as e:
        print(f"{indent}  (could not dir: {e})")
        return
    for a in attrs:
        low = a.lower()
        if any(k in low for k in STAGE_KEYWORDS):
            try:
                val = getattr(obj, a)
                if hasattr(val, "Value"):
                    display = f"{val.Value!r}  [via .Value]"
                elif hasattr(val, "Count"):
                    display = f"Count={val.Count}"
                elif callable(val):
                    display = "(method)"
                else:
                    display = repr(val)
                print(f"{indent}  {a} = {display}")
            except Exception as e:
                print(f"{indent}  {a} -> ERROR: {e}")

def main():
    print("Connecting to HYSYS...")
    hysys = win32.Dispatch("HYSYS.Application")
    hysys.Visible = True
    case = None
    try:
        case = hysys.ActiveSimulationCase
        print(f"Active case: {case.PathName}")
    except Exception:
        case = None
    if not case:
        print(f"Opening {HYSYS_CASE_PATH} ...")
        case = hysys.SimulationCases.Open(HYSYS_CASE_PATH)
    absorber = case.Flowsheet.Operations.Item(ABSORBER_NAME)
    print(f"\nGot absorber: {absorber.Name}")
    show_attrs(absorber, "absorber", depth=0)
    try:
        cf = absorber.ColumnFlowsheet
        show_attrs(cf, "absorber.ColumnFlowsheet", depth=1)
        try:
            ops = cf.Operations
            print(f"\n  absorber.ColumnFlowsheet.Operations.Count = {ops.Count}")
            for i in range(ops.Count):
                try:
                    op = ops.Item(i)
                    try:
                        op_name = op.Name
                    except Exception:
                        op_name = f"<index {i}>"
                    show_attrs(op, f"ColumnFlowsheet.Operations[{i}] ({op_name})", depth=2)
                except Exception as e:
                    print(f"  Could not inspect sub-op {i}: {e}")
        except Exception as e:
            print(f"  ColumnFlowsheet.Operations error: {e}")
        try:
            cs = cf.ColumnStages
            print(f"\n  ColumnStages.Count = {cs.Count}")
            if cs.Count > 0:
                stage0 = cs.Item(0)
                show_attrs(stage0, "ColumnFlowsheet.ColumnStages.Item(0)", depth=2)
        except Exception as e:
            print(f"  ColumnStages error: {e}")
    except Exception as e:
        print(f"  ColumnFlowsheet error: {e}")
    print("\n\n=== DONE ===")

if __name__ == "__main__":
    main()
