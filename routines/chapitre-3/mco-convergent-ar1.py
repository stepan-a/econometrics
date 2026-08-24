"""Un régresseur aléatoire qui biaise les MCO sans les empêcher de converger.

Dans l'AR(1) y_t = ρ y_{t-1} + ε_t, le régresseur y_{t-1} est corrélé aux
erreurs passées mais pas à l'erreur contemporaine. Les MCO sont donc biaisés à
distance finie — le biais est en 1/T, l'approximation classique de Hurwicz vaut
-2ρ/T — mais convergents : le biais s'évanouit quand T croît.

Produit mco-convergent-ar1.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(3105)

N = 50000                          # Nombre d'échantillons
ρ = 0.8                            # Coefficient autorégressif
TAILLES = [10, 20, 50, 100, 200, 500, 1000]

biais = np.zeros(len(TAILLES))
ecarts = np.zeros(len(TAILLES))

for k, T in enumerate(TAILLES):
    # y_0 tiré dans la loi stationnaire, puis récursion vectorisée
    ε = rng.standard_normal((N, T))
    y = np.zeros((N, T+1))
    y[:, 0] = rng.standard_normal(N)/np.sqrt(1-ρ**2)
    for t in range(T):
        y[:, t+1] = ρ*y[:, t] + ε[:, t]
    R = np.sum(y[:, :-1]*y[:, 1:], axis=1)/np.sum(y[:, :-1]**2, axis=1)
    biais[k] = np.mean(R) - ρ
    ecarts[k] = np.std(R)
    print(f"T={T:5d}  biais {biais[k]:+.4f}  (-2ρ/T = {-2*ρ/T:+.4f})"
          f"  écart-type {ecarts[k]:.4f}")

fig, ax = plt.subplots()

ax.plot(TAILLES, biais, 'bo-', markersize=4, label=r"Biais de $\hat\rho$, simulé")
ax.plot(TAILLES, [-2*ρ/T for T in TAILLES], 'r--', linewidth=1,
        label=r"Approximation $-2\rho/T$")
ax.axhline(y=0.0, color='k', linestyle=':', linewidth=1)
ax.fill_between(TAILLES, biais-ecarts, biais+ecarts, color='b', alpha=0.12,
                label=r"$\pm$ un écart-type de $\hat\rho$")

ax.set_xscale('log')
ax.set_xlabel(r"Taille de l'échantillon $T$")
ax.set_ylabel(r'Biais moyen de $\hat\rho$')
ax.legend(loc='lower right', fontsize='small')
fig.tight_layout()

plt.savefig(PGF / 'mco-convergent-ar1.tex', format='pgf')
