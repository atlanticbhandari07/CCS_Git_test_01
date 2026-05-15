import ast
import sys

file_path = r"d:\Motey\Area and cost.py"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    ast.parse(source)
    print("AST parse successful. No syntax error found by ast.parse.")
except SyntaxError as e:
    print(f"SyntaxError detected by ast.parse:")
    print(f"  Message: {e.msg}")
    print(f"  Line: {e.lineno}")
    print(f"  Offset: {e.offset}")
    print(f"  Text: {repr(e.text)}")
except Exception as e:
    print(f"Error: {e}")
