import numpy as np
import matplotlib.pyplot as plt

H0 = 4.0
H_percent = np.array([10, 25, 50, 75, 100])
H_MJ_MVA  = H_percent / 100.0 * H0
zeta = np.array([1.6593, 1.0494, 0.7420, 0.6059, 0.5247])

plt.figure(figsize=(9, 5))
plt.plot(H_MJ_MVA, zeta, color='forestgreen', marker='s', markersize=8, linewidth=2.5,
         label=r'Damping ratio $\zeta$')
for h, z in zip(H_MJ_MVA, zeta):
    plt.annotate(f'{z:.4f}', xy=(h, z), xytext=(4, 6), textcoords='offset points',
                 fontsize=10, color='forestgreen', fontweight='bold')
plt.xlabel(f'Rotational Inertia, H [MJ/MVA] (H₀ = {H0} MJ/MVA = 100%)', fontsize=12, fontweight='bold')
plt.ylabel(r'Damping Ratio, $\zeta$ [-]', fontsize=13, fontweight='bold')
plt.title('Damping Ratio vs Rotational Inertia H', fontsize=14, fontweight='bold')
plt.xticks(H_MJ_MVA)
plt.xlim(0, H0 * 1.1)
plt.ylim(0, max(zeta) * 1.2)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('damping_ratio_only.png', dpi=150)
plt.show()
