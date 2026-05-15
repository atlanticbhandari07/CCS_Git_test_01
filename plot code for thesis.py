import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Update file_path to point to your Excel file
file_path = r"D:\CAPEX sheet for python.xlsx"
df = pd.read_excel(file_path)

print("Columns in file:", df.columns.tolist())

x_col = "Name of Equipment"
y_col = "CAPEX(in Euro)"

df[y_col] = pd.to_numeric(df[y_col], errors='coerce')
df.dropna(subset=[x_col, y_col], inplace=True)
df = df.sort_values(by=y_col, ascending=False)

x = df[x_col].str.replace('/', '/\n').str.replace(' Heat ', '\nHeat ')
y = df[y_col] / 1e6

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
fig, ax = plt.subplots(figsize=(14, 7))

colors = plt.cm.viridis(np.linspace(0.3, 0.7, len(x)))
bars = ax.bar(x, y, color=colors, alpha=0.85, edgecolor='black', linewidth=0.8, width=0.6)

ax.set_ylabel("CAPEX (Million €)", fontsize=14, fontweight='bold')
ax.set_xlabel("")
ax.tick_params(axis='x', rotation=45, labelsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.yaxis.grid(True, linestyle='--', alpha=0.6)
ax.yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.2f} M€'))
ax.set_ylim(0, max(y) * 1.15)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.3f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6), textcoords="offset points",
                ha='center', va='bottom', fontsize=12, fontweight='bold', color='darkblue')

plt.tight_layout()
plt.savefig("equipment_capex_breakdown.pdf", bbox_inches='tight')
print("Plot saved as 'equipment_capex_breakdown.pdf'")
plt.show()
