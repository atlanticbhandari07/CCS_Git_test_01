import pandas as pd
import matplotlib.pyplot as plt

# Update file_path to point to your Excel file
file_path = r"C:\Users\AZ400_ATLANTIC\Desktop\stages with fan manual.xlsx"
df = pd.read_excel(file_path)
print("Columns in file:", df.columns)

x_col = "No. of stages"
y1_col = "CO2 captured Cost(Euro/tons of CO2)"
y2_col = "HOC(MJ/kg of CO2)"
y1_label = r"$CO_2$ captured Cost (€/t $CO_2$)"
y2_label = r"HOC (MJ/kg $CO_2$)"

df[x_col]  = pd.to_numeric(df[x_col],  errors='coerce')
df[y1_col] = pd.to_numeric(df[y1_col], errors='coerce')
df[y2_col] = pd.to_numeric(df[y2_col], errors='coerce')
df.dropna(subset=[x_col, y1_col, y2_col], inplace=True)

x = df[x_col]; y1 = df[y1_col]; y2 = df[y2_col]

fig, ax1 = plt.subplots(figsize=(10, 7))
ax1.plot(x, y1, label=y1_label)
ax1.set_xlabel(x_col, fontsize=14)
ax1.set_xlim(17.5, 25.5)
ax1.set_xticks([18, 19, 20, 21, 22, 23, 24, 25])
ax1.tick_params(axis='x', labelsize=12)
ax1.tick_params(axis='y', labelsize=12)
ax1.set_ylabel(y1_label, fontsize=14)
for xi, yi in zip(x, y1):
    ax1.annotate(f'{yi:.2f}', (xi, yi), textcoords='offset points', xytext=(0, 6), ha='center', fontsize=10)

ax2 = ax1.twinx()
ax2.bar(x, y2, width=0.8, alpha=0.4)
ax2.set_ylabel(y2_label, fontsize=14)
ax2.tick_params(axis='y', labelsize=14)
ax2.set_ylim(bottom=3.0)
for xi, yi in zip(x, y2):
    ax2.annotate(f'{yi:.2f}', (xi, yi), textcoords='offset points', xytext=(0, 6), ha='center', fontsize=12)

ax1.legend(loc='best', fontsize=14)
plt.tight_layout()
plt.show()
