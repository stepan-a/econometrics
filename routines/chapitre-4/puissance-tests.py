"""Ce que les tests d'hétéroscédasticité détectent, et ce qu'ils supposent.

À gauche : puissance de Breusch-Pagan (version studentisée de Koenker), de
White et de Goldfeld-Quandt contre l'intensité γ de l'hétéroscédasticité, dans
y = b0 + b1 x + ε avec V[ε_t] = exp(γ x_t) et des erreurs normales.

À droite : sous H0 (γ = 0) mais avec des erreurs de Student à cinq degrés de
liberté, taux de rejet des quatre tests. La statistique originale de
Breusch-Pagan et celle de Goldfeld-Quandt, qui reposent sur la normalité,
rejettent trois à cinq fois trop souvent — et cela ne s'arrange pas quand T
augmente. Les versions studentisées tiennent leur seuil.

Produit puissance-tests.tex.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from scipy.stats import chi2, f as fisher

from chemins import PGF

rng = np.random.default_rng(4102)

N = 20000                          # Nombre d'échantillons
SEUIL = 0.05
GAMMAS = np.linspace(0.0, 1.0, 11)
T_PUISSANCE = 100                  # Taille d'échantillon du panneau de gauche
TAILLES = [50, 100, 200, 500, 1000]


def mco(X, y):
    """MCO par échantillon : X de forme (n, T, K), y de forme (n, T)."""
    XX = np.einsum('ntk,ntl->nkl', X, X)
    Xy = np.einsum('ntk,nt->nk', X, y)
    # NumPy 2 lit un second opérande à deux indices comme une matrice : on
    # explicite la colonne pour résoudre un système par échantillon.
    b = np.linalg.solve(XX, Xy[..., None])[..., 0]
    return b, y - np.einsum('ntk,nk->nt', X, b)


def r2(g, Z):
    """R² de la régression de g sur Z, la constante étant dans Z."""
    _, u = mco(Z, g)
    centre = g - g.mean(axis=1, keepdims=True)
    return 1 - (u**2).sum(axis=1)/(centre**2).sum(axis=1)


def statistiques(x, y):
    """Les quatre statistiques de test, pour chaque échantillon."""
    n, T = x.shape
    un = np.ones((n, T))
    X = np.stack([un, x], axis=2)
    _, e = mco(X, y)
    e2 = e**2

    Z = X                                        # Régresseurs auxiliaires : 1, x
    ZW = np.stack([un, x, x**2], axis=2)         # White : on ajoute x²

    # Breusch-Pagan original : régression de ê²/σ̂² sur Z, statistique SCE/2.
    σ2 = e2.sum(axis=1)/T                        # Estimateur du MV sous H0
    g = e2/σ2[:, None]
    d = x - x.mean(axis=1, keepdims=True)
    sce = (d*g).sum(axis=1)**2/(d**2).sum(axis=1)
    bp_original = sce/2

    bp_koenker = T*r2(e2, Z)                     # Koenker (1981)
    white = T*r2(e2, ZW)                         # White (1980)

    # Goldfeld-Quandt : on ordonne selon x, on écarte le quart central.
    c = T//4
    m = (T - c)//2
    ordre = np.argsort(x, axis=1)
    xs = np.take_along_axis(x, ordre, axis=1)
    ys = np.take_along_axis(y, ordre, axis=1)
    scr = []
    for tranche in (slice(0, m), slice(T-m, T)):
        Xg = np.stack([np.ones((n, m)), xs[:, tranche]], axis=2)
        _, u = mco(Xg, ys[:, tranche])
        scr.append((u**2).sum(axis=1))
    gq = (scr[1]/(m-2))/(scr[0]/(m-2))

    return bp_original, bp_koenker, white, gq, m


def rejets(T, γ, N, rng, loi='normale', bloc=2000):
    """Taux de rejet des quatre tests, au seuil de 5 %."""
    compte = np.zeros(4)
    fait = 0
    while fait < N:
        n = min(bloc, N - fait)
        x = rng.standard_normal((n, T))
        if loi == 'normale':
            u = rng.standard_normal((n, T))
        else:                                    # Student à 5 ddl, réduite
            u = rng.standard_t(5, size=(n, T))/np.sqrt(5/3)
        y = np.exp(γ*x/2)*u                      # b0 = b1 = 0, V[ε_t] = exp(γ x_t)

        bp0, bpk, w, gq, m = statistiques(x, y)
        c1 = chi2.ppf(1-SEUIL, 1)
        c2 = chi2.ppf(1-SEUIL, 2)
        cf = fisher.ppf(1-SEUIL, m-2, m-2)
        compte += np.array([(bp0 > c1).sum(), (bpk > c1).sum(),
                            (w > c2).sum(), (gq > cf).sum()])
        fait += n
    return compte/N


puissance = np.array([rejets(T_PUISSANCE, γ, N, rng) for γ in GAMMAS])
taille = np.array([rejets(T, 0.0, N, rng, loi='student') for T in TAILLES])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4.0))

courbes = [(1, 'Breusch-Pagan (Koenker)', 'b', 's'),
           (2, 'White', 'g', '^'),
           (3, 'Goldfeld-Quandt', 'm', 'v')]
for j, nom, couleur, marque in courbes:
    ax1.plot(GAMMAS, puissance[:, j], color=couleur, marker=marque,
             markersize=4, linewidth=1, label=nom)
ax1.axhline(y=SEUIL, color='k', linestyle='--', linewidth=1)
ax1.set_xlabel(r"Intensité de l'hétéroscédasticité $\gamma$")
ax1.set_ylabel('Taux de rejet')
ax1.set_title(f'Puissance, erreurs normales, $T={T_PUISSANCE}$', fontsize='medium')
ax1.legend(loc='lower right', fontsize='small', framealpha=1)

courbes = [(0, 'Breusch-Pagan (1979)', 'r', 'o'),
           (1, 'Breusch-Pagan (Koenker)', 'b', 's'),
           (2, 'White', 'g', '^'),
           (3, 'Goldfeld-Quandt', 'm', 'v')]
for j, nom, couleur, marque in courbes:
    ax2.plot(TAILLES, taille[:, j], color=couleur, marker=marque,
             markersize=4, linewidth=1, label=nom)
ax2.axhline(y=SEUIL, color='k', linestyle='--', linewidth=1,
            label='Seuil nominal (5 %)')
ax2.set_xscale('log')
ax2.set_xticks(TAILLES)
ax2.set_xticklabels([str(T) for T in TAILLES])
ax2.xaxis.set_minor_formatter(NullFormatter())
ax2.set_ylim(0, max(0.30, taille.max()*1.1))
ax2.set_xlabel("Taille de l'échantillon $T$")
ax2.set_ylabel('Taux de rejet')
ax2.set_title(r'Taille sous $H_0$, erreurs de Student', fontsize='medium')
ax2.legend(loc='upper left', fontsize='small', framealpha=1)

fig.tight_layout()
plt.savefig(PGF / 'puissance-tests.tex', format='pgf')

print('Puissance (erreurs normales, T = %d) :' % T_PUISSANCE)
for i, γ in enumerate(GAMMAS):
    print('  γ = %.1f : BP-Koenker %.3f  White %.3f  GQ %.3f'
          % (γ, puissance[i, 1], puissance[i, 2], puissance[i, 3]))
print('Taille sous H0 (erreurs de Student à 5 ddl) :')
for i, T in enumerate(TAILLES):
    print('  T = %5d : BP-1979 %.3f  BP-Koenker %.3f  White %.3f  GQ %.3f'
          % (T, taille[i, 0], taille[i, 1], taille[i, 2], taille[i, 3]))
