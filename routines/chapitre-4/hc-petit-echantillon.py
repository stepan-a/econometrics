"""Pourquoi HC0 ne suffit pas quand l'échantillon est petit.

Plan d'expérience à fort levier : le régresseur x prend les quantiles d'une
log-normale, de sorte que quelques observations pèsent très lourd dans
l'estimation. La variance des
erreurs est proportionnelle au régresseur, V[ε_t] ∝ x_t. Le plan étant fixe,
la vraie variance de b1 est connue exactement,

    V[b1] = Σ d_t² σ_t² / (Σ d_t²)²,   d_t = x_t - x̄

ce qui permet de rapporter l'écart-type estimé à l'écart-type vrai. HC0 sous-
estime la dispersion de b1 — d'où le sur-rejet du transparent précédent ; les
corrections HC1, HC2 et HC3 comblent l'écart, HC3 le surcompensant même.

Produit hc-petit-echantillon.tex.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from scipy.stats import norm

from chemins import PGF

rng = np.random.default_rng(4103)

N = 40000                          # Nombre d'échantillons par taille
TAILLES = [20, 30, 50, 100, 200, 500]


def rapport(T, N, rng, bloc=4000):
    """E[écart-type estimé]/écart-type vrai, pour HC0 à HC3, et levier maximal."""
    # Plan fixe et déterministe : les quantiles d'une log-normale. La forme du
    # plan est ainsi la même à toutes les tailles, et la courbe n'isole que
    # l'effet de T sur les leviers.
    x = np.exp(norm.ppf((np.arange(T) + 0.5)/T))
    σ2 = x/x.mean()                         # V[ε_t] ∝ x_t, normalisée à 1 en moyenne
    d = x - x.mean()
    Sdd = (d**2).sum()
    h = 1/T + d**2/Sdd                      # Leviers de la matrice chapeau
    vraie = np.sqrt((d**2*σ2).sum()/Sdd**2)

    cumul = np.zeros(4)
    fait = 0
    while fait < N:
        n = min(bloc, N - fait)
        y = np.sqrt(σ2)*rng.standard_normal((n, T))   # b0 = b1 = 0
        b1 = (d*y).sum(axis=1)/Sdd
        b0 = y.mean(axis=1) - b1*x.mean()
        e = y - b0[:, None] - b1[:, None]*x

        base = d**2*e**2
        v = np.stack([base.sum(axis=1)/Sdd**2,                     # HC0
                      T/(T-2)*base.sum(axis=1)/Sdd**2,             # HC1
                      (base/(1-h)).sum(axis=1)/Sdd**2,             # HC2
                      (base/(1-h)**2).sum(axis=1)/Sdd**2])         # HC3
        cumul += np.sqrt(v).sum(axis=1)
        fait += n
    return cumul/N/vraie, h.max()


resultats = [rapport(T, N, rng) for T in TAILLES]
rapports = np.array([r for r, _ in resultats])
leviers = np.array([h for _, h in resultats])

fig, ax = plt.subplots()
styles = [('HC0 (White)', 'b', 's'),
          ('HC1', 'r', 'o'),
          ('HC2', 'c', 'D'),
          ('HC3', 'g', '^')]
for j, (nom, couleur, marque) in enumerate(styles):
    ax.plot(TAILLES, rapports[:, j], color=couleur, marker=marque,
            markersize=4, linewidth=1, label=nom)
ax.axhline(y=1.0, color='k', linestyle='--', linewidth=1,
           label='Écart-type vrai')

ax.set_xscale('log')
ax.set_xticks(TAILLES)
ax.set_xticklabels([str(T) for T in TAILLES])
ax.xaxis.set_minor_formatter(NullFormatter())
# On dégage le haut du cadre pour que la légende ne recouvre aucune courbe.
ax.set_ylim(0.45, 1.45)
ax.set_xlabel("Taille de l'échantillon $T$")
ax.set_ylabel(r'Écart-type estimé rapporté au vrai')
ax.legend(loc='upper right', fontsize='small', framealpha=1)
fig.tight_layout()

plt.savefig(PGF / 'hc-petit-echantillon.tex', format='pgf')

for i, T in enumerate(TAILLES):
    print('T = %4d (levier max %.2f) : HC0 %.3f  HC1 %.3f  HC2 %.3f  HC3 %.3f'
          % (T, leviers[i], rapports[i, 0], rapports[i, 1],
             rapports[i, 2], rapports[i, 3]))
