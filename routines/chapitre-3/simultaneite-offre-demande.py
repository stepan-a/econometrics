"""Ce que les MCO estiment sur un marché où le prix est déterminé à l'équilibre.

Demande  : Q = a0 + a1 P + a2 R + u,  a1 < 0
Offre    : Q = b0 + b1 P + b2 W + v,  b1 > 0

Le prix d'équilibre dépend de u : régresser Q sur P (et R) ne restitue pas la
pente de la demande, la droite des MCO est attirée par la courbe d'offre.

Produit simultaneite-offre-demande.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(3102)

T = 300                            # Taille de l'échantillon
a0, a1, a2 = 10.0, -1.0, 0.5       # Demande : constante, prix, revenu
b0, b1, b2 = -2.0, 1.0, -0.5       # Offre : constante, prix, coût des inputs
σu, σv = 1.0, 1.0                  # Écarts-type des deux chocs

R = 2.0 + rng.standard_normal(T)   # Revenu des consommateurs
W = 2.0 + rng.standard_normal(T)   # Coût des inputs
u = σu*rng.standard_normal(T)      # Choc de demande
v = σv*rng.standard_normal(T)      # Choc d'offre

# Prix et quantité d'équilibre
P = ((b0-a0) + b2*W - a2*R + (v-u))/(a1-b1)
Q = a0 + a1*P + a2*R + u

# MCO de Q sur (1, P, R) : la pente sur P est censée estimer a1
X = np.column_stack([np.ones(T), P, R])
mco = np.linalg.lstsq(X, Q, rcond=None)[0]

# Variables instrumentales, avec Z = (1, R, W)
Z = np.column_stack([np.ones(T), R, W])
vi = np.linalg.solve(Z.T @ X, Z.T @ Q)

fig, ax = plt.subplots()

ax.plot(P, Q, '.', color='0.55', markersize=3, label="Équilibres observés")

p = np.linspace(np.min(P), np.max(P), 2)
Rbar = np.mean(R)
Wbar = np.mean(W)
ax.plot(p, a0 + a1*p + a2*Rbar, 'k-', linewidth=1.5,
        label=fr"Demande, $\alpha_1={a1:.2f}$")
ax.plot(p, b0 + b1*p + b2*Wbar, 'k--', linewidth=1,
        label=fr"Offre, $\beta_1={b1:.2f}$")
ax.plot(p, mco[0] + mco[1]*p + mco[2]*Rbar, 'r-', linewidth=1.5,
        label=fr"MCO, pente {mco[1]:.2f}")
ax.plot(p, vi[0] + vi[1]*p + vi[2]*Rbar, 'b-', linewidth=1.5,
        label=fr"VI, pente {vi[1]:.2f}")

ax.set_xlabel(r'Prix $P_t$')
ax.set_ylabel(r'Quantité $Q_t$')
ax.legend(loc='upper right', fontsize='small')
fig.tight_layout()

plt.savefig(PGF / 'simultaneite-offre-demande.tex', format='pgf')
print(f"MCO {mco[1]:.3f}   VI {vi[1]:.3f}   vrai {a1:.3f}")
