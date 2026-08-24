"""MCG contre MCO sous hétéroscédasticité à poids connus.

Dispositif de l'exercice 2 du partiel 2024 : V[ε_i] = σ² z_i², avec z observée
et indépendante de x. Les deux estimateurs sont sans biais, le MCG est plus
précis.

Produit mcg-vs-mco.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(2211)

N = 20000                          # Nombre d'échantillons
T = 40                             # Taille de chaque échantillon
b0, b1 = 1.0, 0.5                  # Vraies valeurs des paramètres

x = 10*rng.uniform(size=T)         # Variable explicative déterministe
z = 1 + 9*rng.uniform(size=T)      # Poids observés, indépendants de x
w = z**2                           # V[ε_i] = σ² z_i²

X = np.column_stack([np.ones(T), x])
XX = np.linalg.inv(X.T @ X)                    # MCO
Wi = np.diag(1/w)
XWX = np.linalg.inv(X.T @ Wi @ X)              # MCG

Bo = np.zeros(N)                   # MCO
Bg = np.zeros(N)                   # MCG

for i in range(N):
    y = b0 + b1*x + np.sqrt(w)*rng.standard_normal(T)
    Bo[i] = (XX @ (X.T @ y))[1]
    Bg[i] = (XWX @ (X.T @ Wi @ y))[1]

fig, ax = plt.subplots()
ax.hist(Bo, bins='auto', density=True, histtype='step', color='b',
        label=f"MCO (écart-type {np.std(Bo):.3f})")
ax.hist(Bg, bins='auto', density=True, histtype='step', color='g',
        label=f"MCG (écart-type {np.std(Bg):.3f})")
ax.axvline(x=b1, color='r', linestyle='--', linewidth=1,
           label=r'Vraie valeur $\beta_1$')
ax.set_xlabel(r'$b_1$')
ax.set_ylabel('Densité')
ax.legend(loc='upper left', fontsize='small')
fig.tight_layout()

plt.savefig(PGF / 'mcg-vs-mco.tex', format='pgf')
