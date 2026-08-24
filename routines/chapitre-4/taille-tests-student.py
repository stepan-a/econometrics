"""Ce que l'hétéroscédasticité fait au test de Student.

Modèle y = b0 + b1 x + ε sous H0 (b1 = 0), avec V[ε_t] = exp(γ x_t) : la
dispersion des erreurs croît avec le régresseur. On teste H0 au seuil nominal
de 5 %, en estimant la variance de b1 de trois façons : la formule usuelle
s²(X'X)⁻¹, le sandwich HC0 de White, et sa correction HC3. Seul le taux de
rejet des estimateurs robustes rejoint les 5 % annoncés.

Produit taille-tests-student.tex.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from scipy.stats import t as student

from chemins import PGF

rng = np.random.default_rng(4101)

N = 40000                          # Nombre d'échantillons par taille
TAILLES = [20, 30, 50, 100, 200, 500, 1000, 2000]
γ = 1.5                            # Intensité de l'hétéroscédasticité
SEUIL = 0.05                       # Seuil nominal du test


def taux_de_rejet(T, N, rng, bloc=2000):
    """Taux de rejet de H0 : b1 = 0, pour chaque estimateur de la variance."""
    rejets = np.zeros(3)
    fait = 0
    critique = student.ppf(1 - SEUIL/2, T-2)
    while fait < N:
        n = min(bloc, N - fait)
        x = rng.standard_normal((n, T))
        σ = np.exp(γ*x/2)                       # V[ε_t] = exp(γ x_t)
        ε = σ*rng.standard_normal((n, T))
        y = ε                                   # b0 = b1 = 0 sous H0

        # Estimateur de la pente : combinaison linéaire des y_t, de poids
        # d_t/Σd², avec d_t l'écart de x_t à sa moyenne (théorème FWL).
        d = x - x.mean(axis=1, keepdims=True)
        Sdd = (d**2).sum(axis=1)
        b1 = (d*y).sum(axis=1)/Sdd
        b0 = y.mean(axis=1) - b1*x.mean(axis=1)
        e = y - b0[:, None] - b1[:, None]*x

        h = 1/T + d**2/Sdd[:, None]             # Leviers de la matrice chapeau
        s2 = (e**2).sum(axis=1)/(T-2)

        v = np.empty((3, n))
        v[0] = s2/Sdd                                              # usuelle
        v[1] = (d**2*e**2).sum(axis=1)/Sdd**2                      # HC0
        v[2] = (d**2*e**2/(1-h)**2).sum(axis=1)/Sdd**2             # HC3

        rejets += (np.abs(b1)/np.sqrt(v) > critique).sum(axis=1)
        fait += n
    return rejets/N


taux = np.array([taux_de_rejet(T, N, rng) for T in TAILLES])

fig, ax = plt.subplots()
styles = [('Écart-type usuel', 'r', 'o'),
          ('HC0 (White)', 'b', 's'),
          ('HC3', 'g', '^')]
for j, (nom, couleur, marque) in enumerate(styles):
    ax.plot(TAILLES, taux[:, j], color=couleur, marker=marque,
            markersize=4, linewidth=1, label=nom)
ax.axhline(y=SEUIL, color='k', linestyle='--', linewidth=1,
           label='Seuil nominal (5 %)')

ax.set_xscale('log')
ax.set_xticks(TAILLES)
ax.set_xticklabels([str(T) for T in TAILLES])
# Sans cela, l'échelle logarithmique ajoute ses propres étiquettes mineures
# (« 3×10¹ », « 4×10¹ », ...) par-dessus les tailles d'échantillon.
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_ylim(0, max(0.30, taux.max()*1.1))
ax.set_xlabel("Taille de l'échantillon $T$")
ax.set_ylabel('Taux de rejet de $H_0$')
ax.legend(loc='center right', fontsize='small', framealpha=1)
fig.tight_layout()

plt.savefig(PGF / 'taille-tests-student.tex', format='pgf')

for i, T in enumerate(TAILLES):
    print('T = %5d : usuel %.3f   HC0 %.3f   HC3 %.3f'
          % (T, taux[i, 0], taux[i, 1], taux[i, 2]))
