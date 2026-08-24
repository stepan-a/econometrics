"""Biais d'atténuation induit par une erreur de mesure sur la variable explicative.

Le modèle de la nature est y = α + βx + v, mais on n'observe x qu'à un bruit
près : x* = x + u. Régresser y sur x* tire la pente estimée vers zéro, dans le
rapport σ_x²/(σ_x²+σ_u²) donné par le théorème du chapitre.

Produit attenuation-erreur-mesure.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(3101)

N = 20000                          # Nombre d'échantillons
T = 200                            # Taille de chaque échantillon
α, β = 1.0, 1.0                    # Constante et pente du modèle de la nature
σx = 1.0                           # Écart-type de la variable explicative
σv = 0.5                           # Écart-type des perturbations

fig, ax = plt.subplots()

colours = ['b', 'g', 'r']

for k, σu in enumerate([0.0, np.sqrt(0.5), np.sqrt(2.0)]):
    B = np.zeros(N)
    for i in range(N):
        x = σx*rng.standard_normal(T)
        y = α + β*x + σv*rng.standard_normal(T)
        # L'économètre n'observe pas x mais x*, mesuré avec erreur
        xs = x + σu*rng.standard_normal(T)
        xc = xs - np.mean(xs)
        B[i] = np.dot(y-np.mean(y), xc)/np.dot(xc, xc)
    # Limite en probabilité prédite par le théorème d'atténuation
    limite = β*σx**2/(σx**2+σu**2)
    ax.hist(B, bins='auto', density=True, histtype='step', color=colours[k],
            label=fr"$\sigma_u^2={σu**2:.1f}$ (plim {limite:.2f}, moyenne {np.mean(B):.2f})")
    ax.axvline(x=limite, color=colours[k], linestyle=':', linewidth=1)

ax.axvline(x=β, color='k', linestyle='--', linewidth=1, label=r'Vraie valeur $\beta$')
ax.set_xlabel(r'$\hat b$')
ax.set_ylabel('Densité')
ax.legend(loc='upper left', fontsize='small')
fig.tight_layout()

plt.savefig(PGF / 'attenuation-erreur-mesure.tex', format='pgf')
