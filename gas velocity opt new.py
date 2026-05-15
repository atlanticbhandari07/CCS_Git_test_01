import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

v_base = 2.0
p_fan_base = 110
absorber_capex_base = 1.03e7
absorber_area_base = 39.18
fan_capex_base = 6.877e5
fan_capacity_base = 190800
fan_opex_base = 268600
scaling_exponent = 0.6
ANNUALIZATION_FACTOR_AF = 11.15
n = 2

velocities = np.arange(1.8, 2.5 + 0.1, 0.1)
absorber_area = absorber_area_base * (v_base / velocities)
absorber_capex = absorber_capex_base * (absorber_area / absorber_area_base) ** scaling_exponent
p_fan = p_fan_base * (velocities / v_base) ** n
fan_capex = fan_capex_base * (velocities / v_base) ** scaling_exponent
fan_opex = fan_opex_base * (velocities / v_base) ** 2
abs_capex_ann = absorber_capex / ANNUALIZATION_FACTOR_AF
fan_capex_ann = fan_capex / ANNUALIZATION_FACTOR_AF
total_cost = abs_capex_ann + fan_capex_ann + fan_opex

opt_index = np.argmin(total_cost)
opt_velocity = velocities[opt_index]
opt_total_cost = total_cost[opt_index]

print(f"Optimum velocity: {opt_velocity:.2f} m/s")
print(f"Minimum annualized total cost: {opt_total_cost:,.2f} €/yr")

mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 13

colors = ['#5DADE2', '#E67E22', '#27AE60']
x = np.arange(len(velocities))
vel_labels = [f"{v:.1f} m/s" for v in velocities]

fig, ax = plt.subplots(figsize=(11, 7))
bars1 = ax.bar(x, abs_capex_ann, color=colors[0], label='Annualized Absorber CAPEX', edgecolor='white', linewidth=0.6)
bars2 = ax.bar(x, fan_capex_ann, color=colors[1], label='Annualized Fan CAPEX', edgecolor='white', linewidth=0.6, bottom=abs_capex_ann)
bars3 = ax.bar(x, fan_opex, color=colors[2], label='Annual Fan OPEX', edgecolor='white', linewidth=0.6, bottom=abs_capex_ann + fan_capex_ann)

for i in range(len(velocities)):
    ax.text(x[i], abs_capex_ann[i]/2, f'{abs_capex_ann[i]/1e6:.3f} M€',
            ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    ax.text(x[i], abs_capex_ann[i] + fan_capex_ann[i]/2, f'{fan_capex_ann[i]/1e6:.3f} M€',
            ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    ax.text(x[i], abs_capex_ann[i] + fan_capex_ann[i] + fan_opex[i]/2, f'{fan_opex[i]/1e6:.3f} M€',
            ha='center', va='center', fontsize=12, color='white', fontweight='bold')

for i, total in enumerate(total_cost):
    ax.text(x[i], total + 0.005e6, f'{total/1e6:.3f} M€/yr',
            ha='center', va='bottom', fontsize=13, fontweight='bold', color='black')

ax.axhline(y=opt_total_cost, color='black', linestyle=':', linewidth=1.8,
           label=f'Optimum: {opt_total_cost/1e6:.3f} M€/yr @ {opt_velocity:.1f} m/s')
ax.set_xticks(x)
ax.set_xticklabels(vel_labels, fontsize=13)
ax.set_xlabel("Superficial Gas Velocity in Absorber column (m/s)", fontsize=15, fontweight='bold')
ax.set_ylabel("Annualized Total Cost (Million €/year)", fontsize=15, fontweight='bold')
ax.legend(loc='lower left', fontsize=12, framealpha=0.9)
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f'{v/1e6:.2f} M€'))
ax.grid(True, axis='y', alpha=0.3, linestyle='--')
fig.tight_layout()
plt.show()
