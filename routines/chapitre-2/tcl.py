"""Théorème central limite : moyenne standardisée d'une loi exponentielle.

Produit tcl.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(2211)

N = 50000                          # Nombre de répétitions

fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

grille = np.linspace(-4, 4, 400)
densite = np.exp(-grille**2/2)/np.sqrt(2*np.pi)

for ax, n in zip(axes, [1, 5, 30]):
    # Exponentielle de paramètre 1 : espérance 1, variance 1
    X = rng.exponential(size=(N, n))
    Z = np.sqrt(n)*(np.mean(X, axis=1) - 1.0)
    ax.hist(Z, bins=120, range=(-4, 4), density=True, histtype='step', color='b')
    ax.plot(grille, densite, 'r-', linewidth=1)
    ax.set_title(f'n = {n}', fontsize='medium')
    ax.set_xlabel(r'$\sqrt{n}\,(\bar X - \mu)$')

axes[0].set_ylabel('Densité')
fig.tight_layout()

plt.savefig(PGF / 'tcl.tex', format='pgf')
