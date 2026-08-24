"""Normalité asymptotique de l'estimateur des MCO sous erreurs non normales.

Les erreurs sont log-normales centrées, donc très asymétriques. À T petit la
distribution de b̂ ne l'est pas non plus ; le théorème central limite la ramène
vers la loi normale quand T croît.

Produit normalite-asymptotique-bhat.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(2211)

N = 30000                          # Nombre d'échantillons

fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

grille = np.linspace(-4, 4, 400)
densite = np.exp(-grille**2/2)/np.sqrt(2*np.pi)

for ax, T in zip(axes, [5, 15, 200]):
    x = 10*rng.uniform(size=T)
    xc = x - np.mean(x)
    B = np.zeros(N)
    for i in range(N):
        # Erreurs log-normales centrées : E[ε]=0, forte asymétrie
        ε = np.exp(rng.standard_normal(T)) - np.exp(0.5)
        y = ε
        B[i] = np.dot(y-np.mean(y), xc)/np.dot(xc, xc)
    Z = (B - np.mean(B))/np.std(B)     # Estimateur centré réduit
    ax.hist(Z, bins=120, range=(-4, 4), density=True, histtype='step', color='b')
    ax.plot(grille, densite, 'r-', linewidth=1)
    ax.set_title(f'T = {T}', fontsize='medium')
    ax.set_xlabel(r'$\hat b_1$ centré réduit')

axes[0].set_ylabel('Densité')
fig.tight_layout()

plt.savefig(PGF / 'normalite-asymptotique-bhat.tex', format='pgf')
