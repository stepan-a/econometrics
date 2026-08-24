"""Biais de variable omise, selon la corrélation entre variable incluse et omise.

Calibration sur l'équation de salaire du chapitre 1 : x1 = éducation,
x2 = talent (inobservé), β1 = 0,09 le rendement d'une année d'études.
Le biais théorique vaut β2 × corr(x1,x2) puisque les régresseurs sont réduits.

Produit biais-variable-omise.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(2211)

N = 4000                           # Nombre d'échantillons
T = 100                            # Taille de chaque échantillon
b1, b2 = 0.09, 0.05                # Rendement de l'éducation, effet du talent
σ = 0.4                            # Écart-type des perturbations

fig, ax = plt.subplots()

colours = ['b', 'g', 'r']

for k, ρ in enumerate([0.0, 0.5, 0.9]):
    B = np.zeros(N)
    for i in range(N):
        talent = rng.standard_normal(T)
        educ = ρ*talent + np.sqrt(1-ρ**2)*rng.standard_normal(T)
        y = b1*educ + b2*talent + σ*rng.standard_normal(T)
        xc = educ - np.mean(educ)
        # Le talent est omis : on régresse y sur la seule variable educ
        B[i] = np.dot(y-np.mean(y), xc)/np.dot(xc, xc)
    ax.hist(B, bins='auto', density=True, histtype='step', color=colours[k],
            label=f"corr = {ρ:.1f} (biais {np.mean(B)-b1:+.3f})")

ax.axvline(x=b1, color='k', linestyle='--', linewidth=1, label=r'Vraie valeur $\beta_1$')
ax.set_xlabel(r'$\hat b_1$')
ax.set_ylabel('Densité')
ax.legend(loc='upper right', fontsize='small')
fig.tight_layout()

plt.savefig(PGF / 'biais-variable-omise.tex', format='pgf')
