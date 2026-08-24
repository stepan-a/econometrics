"""Moindres carrés pondérés : ce que la pondération rapporte, et ce qu'elle coûte
quand le modèle de variance est faux.

Modèle y = b0 + b1 x + ε, avec V[ε_t] = exp(γ x_t) : c'est le dispositif du
transparent sur la taille du test de Student. Trois estimateurs de b1 :

  - les MCO ;
  - les MCP fondés sur le bon modèle de variance, dont les poids sont estimés
    en régressant log ê² sur x (procédure de Harvey) ;
  - les MCP fondés sur un modèle de variance faux, dont les poids sont estimés
    en régressant log ê² sur une variable v sans rapport avec la variance.

Les trois sont centrés sur b1 : se tromper de modèle de variance ne biaise pas
l'estimateur. Mais seuls les MCP correctement spécifiés gagnent en précision ;
les MCP mal spécifiés font aussi mal que les MCO. Le script imprime en outre
l'écart-type usuel moyen de chaque estimateur, à comparer à sa dispersion
effective : après pondération par de mauvais poids, la formule usuelle reste
fausse.

Produit mcp-vs-mco.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(4104)

N = 40000                          # Nombre d'échantillons
T = 100                            # Taille de chaque échantillon
b0, b1 = 1.0, 0.5                  # Vraies valeurs des paramètres
γ = 1.5                            # V[ε_t] = exp(γ x_t)


def pente_mcp(x, y, w):
    """Pente et variance usuelle des MCP, par échantillon."""
    Sw = w.sum(axis=1)
    Swx = (w*x).sum(axis=1)
    Swxx = (w*x**2).sum(axis=1)
    Swy = (w*y).sum(axis=1)
    Swxy = (w*x*y).sum(axis=1)
    det = Sw*Swxx - Swx**2
    p1 = (Sw*Swxy - Swx*Swy)/det
    p0 = (Swxx*Swy - Swx*Swxy)/det
    e = y - p0[:, None] - p1[:, None]*x
    s2 = (w*e**2).sum(axis=1)/(T-2)
    return p1, s2*Sw/det


def poids(x, y, e, u):
    """Poids de Harvey : régression de log ê² sur la variable u."""
    g = np.log(e**2 + 1e-12)
    d = u - u.mean(axis=1, keepdims=True)
    pente = (d*(g - g.mean(axis=1, keepdims=True))).sum(axis=1)/(d**2).sum(axis=1)
    # La constante de la régression est sans effet sur les MCP : seuls comptent
    # les poids relatifs. La correction de biais de Harvey y est absorbée.
    return np.exp(-pente[:, None]*u)


B = np.zeros((3, N))
V = np.zeros((3, N))
fait = 0
while fait < N:
    n = min(4000, N - fait)
    tranche = slice(fait, fait + n)
    x = rng.standard_normal((n, T))
    v = rng.standard_normal((n, T))               # Variable sans rapport
    y = b0 + b1*x + np.exp(γ*x/2)*rng.standard_normal((n, T))

    un = np.ones((n, T))
    B[0, tranche], V[0, tranche] = pente_mcp(x, y, un)          # MCO
    p1 = B[0, tranche]
    p0 = y.mean(axis=1) - p1*x.mean(axis=1)
    e = y - p0[:, None] - p1[:, None]*x

    B[1, tranche], V[1, tranche] = pente_mcp(x, y, poids(x, y, e, x))
    B[2, tranche], V[2, tranche] = pente_mcp(x, y, poids(x, y, e, v))
    fait += n

fig, ax = plt.subplots()
styles = [('MCO', 'b'), ('MCP, variance bien spécifiée', 'g'),
          ('MCP, variance mal spécifiée', 'r')]
for j, (nom, couleur) in enumerate(styles):
    ax.hist(B[j], bins='auto', density=True, histtype='step', color=couleur,
            label=f"{nom} (écart-type {np.std(B[j]):.3f})")
ax.axvline(x=b1, color='k', linestyle='--', linewidth=1,
           label=r'Vraie valeur $\beta_1$')

ax.set_xlim(b1-1.2, b1+1.2)
ax.set_xlabel(r'Estimation de la pente $\beta_1$')
ax.set_ylabel('Densité')
ax.legend(loc='upper left', fontsize='small', framealpha=1)
fig.tight_layout()

plt.savefig(PGF / 'mcp-vs-mco.tex', format='pgf')

for j, (nom, _) in enumerate(styles):
    print('%-30s moyenne %.3f  écart-type %.3f  écart-type usuel moyen %.3f'
          % (nom, np.mean(B[j]), np.std(B[j]), np.mean(np.sqrt(V[j]))))
