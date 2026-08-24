"""Trois formes d'erreurs : sphériques, hétéroscédastiques, autocorrélées.

Produit erreurs-non-spheriques.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(2211)

T = 200                            # Taille de l'échantillon

x = 10*rng.uniform(size=T)
x.sort()

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Erreurs sphériques : dispersion constante
ε = rng.standard_normal(T)
axes[0].scatter(x, ε, marker='o', facecolors='none', edgecolor='black', s=12)
axes[0].set_title('Sphériques', fontsize='medium')
axes[0].set_xlabel('x')

# Hétéroscédasticité : la dispersion croît avec x
ε = (0.15*x)*rng.standard_normal(T)
axes[1].scatter(x, ε, marker='o', facecolors='none', edgecolor='black', s=12)
axes[1].set_title('Hétéroscédastiques', fontsize='medium')
axes[1].set_xlabel('x')

# Autocorrélation : processus AR(1), représenté contre le temps
φ = 0.9
ε = np.zeros(T)
ν = rng.standard_normal(T)
for t in range(1, T):
    ε[t] = φ*ε[t-1] + ν[t]
axes[2].plot(np.arange(T), ε, color='black', linewidth=.8)
axes[2].set_title(f'Autocorrélées (AR(1), $\\varphi$ = {φ})', fontsize='medium')
axes[2].set_xlabel('t')

axes[0].set_ylabel(r'$\varepsilon$')
fig.tight_layout()

plt.savefig(PGF / 'erreurs-non-spheriques.tex', format='pgf')
