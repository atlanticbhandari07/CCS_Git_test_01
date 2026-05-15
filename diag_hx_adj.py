import win32com.client as win32

def diag():
    try:
        print("Connecting to HYSYS...")
        hysys = win32.Dispatch("HYSYS.Application")
        case = hysys.ActiveDocument or hysys.SimulationCases.Item(0)
        hx_name = "E-100"
        try:
            hx = case.Flowsheet.Operations.Item(hx_name)
            print(f"\n--- HX: {hx_name} ---")
            props = dir(hx)
            for p in ["InletStreams", "OutletStreams", "FeedStreams", "ProductStreams"]:
                if p in props:
                    coll = getattr(hx, p)
                    print(f"{p}: {[coll.Item(i).name for i in range(coll.Count)]}")
        except:
            print(f"Could not find or inspect HX {hx_name}")
        adj_name = "ADJ-2"
        try:
            adj = case.Flowsheet.Operations.Item(adj_name)
            print(f"\n--- Adjust: {adj_name} ---")
            print(f"Target Value: {adj.TargetValue.Value if hasattr(adj.TargetValue, 'Value') else '?'}")
        except:
            print(f"Could not find or inspect Adjust {adj_name}")
    except Exception as e:
        print(f"Diagnostic failed: {e}")

if __name__ == "__main__":
    diag()
