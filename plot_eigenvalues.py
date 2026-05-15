"""
Eigenvalue Plot - Due to Variation of Rotational Inertia H
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

H0 = 4.0
H_percent = np.array([10, 25, 50, 75, 100])
H_MJ_MVA  = H_percent / 100.0 * H0

sigma_lam1 = np.array([-0.3938, -0.1575, -0.0788, -0.0525, -0.3938])
sigma_lam2 = np.array([-0.3938, -0.1575, -0.0788, -0.0525, -0.3938])
omega_lam1 = np.array([-34.4304, -21.7766, -15.3986, -12.5729, -34.4304])
omega_lam2 = np.array([ 34.4304,  21.7766,  15.3986,  12.5729,  34.4304])
zeta    = np.array([1.1435, 1.7232, 0.5114, 0.4176, 0.3616])
f_Hz    = np.array([5.4798, 3.4658, 2.4508, 2.0010, 1.1435])
omega_d = np.array([34.4304, 21.7766, 15.3986, 12.5729, 10.8885])

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(H_MJ_MVA, sigma_lam1, color='royalblue', marker='o', markersize=5, linewidth=2,
        label=r'Real part $\sigma$ of λ₁ & λ₂')
ax.plot(H_MJ_MVA, omega_lam1, color='crimson', marker='x', markersize=7, linewidth=2, linestyle='--',
        label=r'Imag part $\omega_d$ of λ₁')
ax.plot(H_MJ_MVA, omega_lam2, color='darkorange', marker='x', markersize=7, linewidth=2, linestyle='-.',
        label=r'Imag part $\omega_d$ of λ₂')
ax.axhline(0, color='gray', linewidth=0.8, linestyle=':')
ax.set_xlabel('Rotational Inertia, H [MJ/MVA]', fontsize=13, fontweight='bold')
ax.set_ylabel('Eigenvalues Components', fontsize=13, fontweight='bold')
ax.set_title('Plot of Eigenvalues due to the Vary of H', fontsize=14, fontweight='bold')
ax.set_xlim(0, H0 * 1.15)
ax.set_ylim(-42, 42)
ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)
ax.legend(fontsize=11, loc='upper right')
plt.tight_layout()
plt.savefig('eigenvalue_plot.png', dpi=150, bbox_inches='tight')
plt.show()
