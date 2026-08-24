"""Le prix des variables instrumentales : convergent, mais moins précis.

Modèle y = βx + ε avec x endogène (corr(x,ε) = 0,4) et un instrument z valide,
corrélé à x. Les MCO sont concentrés, mais au mauvais endroit ; les VI sont
centrées sur β, au prix d'une dispersion nettement plus grande.

Produit vi-vs-mco.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(3103)

N = 20000                          # Nombre d'échantillons
T = 200                            # Taille de chaque échantillon
β = 1.0                            # Pente du modèle de la nature
π = 0.6                            # Force de l'instrument : x = π z + ...
ρ = 0.4                            # Corrélation entre x et l'erreur

MCO = np.zeros(N)
VI = np.zeros(N)

for i in range(N):
    z = rng.standard_normal(T)
    # Partie de x non expliquée par l'instrument, corrélée à l'erreur
    e = rng.standard_normal(T)
    w = rng.standard_normal(T)
    ε = e
    ξ = ρ*e + np.sqrt(1-ρ**2)*w
    x = π*z + np.sqrt(1-π**2)*ξ
    y = β*x + ε
    MCO[i] = np.dot(x, y)/np.dot(x, x)
    VI[i] = np.dot(z, y)/np.dot(z, x)

fig, ax = plt.subplots()

ax.hist(MCO, bins='auto', density=True, histtype='step', color='r',
        label=fr"MCO (moyenne {np.mean(MCO):.2f}, écart-type {np.std(MCO):.2f})")
ax.hist(VI, bins='auto', density=True, histtype='step', color='b',
        label=fr"VI (moyenne {np.mean(VI):.2f}, écart-type {np.std(VI):.2f})")
ax.axvline(x=β, color='k', linestyle='--', linewidth=1, label=r'Vraie valeur $\beta$')

ax.set_xlim(β-1.0, β+1.0)
ax.set_xlabel('Estimation de la pente')
ax.set_ylabel('Densité')
ax.legend(loc='upper left', fontsize='small')
fig.tight_layout()

plt.savefig(PGF / 'vi-vs-mco.tex', format='pgf')
print(f"MCO {np.mean(MCO):.3f} ({np.std(MCO):.3f})  VI {np.mean(VI):.3f} ({np.std(VI):.3f})")
