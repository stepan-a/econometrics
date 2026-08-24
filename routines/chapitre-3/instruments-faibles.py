"""Ce que devient l'estimateur des VI quand l'instrument est faible.

Même expérience que vi-vs-mco.py, mais on fait varier la force π de
l'instrument dans la première étape x = π z + ... Quand π s'effondre, la loi de
l'estimateur des VI développe des queues épaisses et sa masse se déplace vers
la limite en probabilité des MCO : l'instrument faible ne corrige plus rien.

On trace la médiane plutôt que la moyenne : à instrument faible, l'estimateur
des VI n'a pas de moment d'ordre un dans le cas juste identifié.

Produit instruments-faibles.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import PGF

rng = np.random.default_rng(3104)

N = 20000                          # Nombre d'échantillons
T = 200                            # Taille de chaque échantillon
β = 1.0                            # Pente du modèle de la nature
ρ = 0.4                            # Corrélation entre x et l'erreur

fig, ax = plt.subplots()

colours = ['b', 'g', 'r']
π_faible = 0.05
# Grille de classes commune aux trois expériences, pour qu'elles se comparent
BORNES = np.linspace(β-2.0, β+2.0, 161)

for k, π in enumerate([0.5, 0.15, π_faible]):
    VI = np.zeros(N)
    F = np.zeros(N)
    for i in range(N):
        z = rng.standard_normal(T)
        e = rng.standard_normal(T)
        w = rng.standard_normal(T)
        ε = e
        ξ = ρ*e + np.sqrt(1-ρ**2)*w
        x = π*z + np.sqrt(1-π**2)*ξ
        y = β*x + ε
        VI[i] = np.dot(z, y)/np.dot(z, x)
        # Statistique F de la première étape (régression de x sur z)
        p = np.dot(z, x)/np.dot(z, z)
        r = x - p*z
        F[i] = (T-1)*p**2*np.dot(z, z)/np.dot(r, r)
    ax.hist(VI, bins=BORNES, density=True, histtype='step', color=colours[k],
            label=fr"$\pi={π:.2f}$ ($F$ médian {np.median(F):.0f},"
                  fr" médiane {np.median(VI):.2f})")
    print(f"π={π:.2f}  F médian {np.median(F):6.1f}  médiane VI {np.median(VI):.3f}"
          f"  |erreur|>1 : {np.mean(np.abs(VI-β) > 1):.1%}")

ax.axvline(x=β, color='k', linestyle='--', linewidth=1, label=r'Vraie valeur $\beta$')
# Limite en probabilité des MCO, vers laquelle l'estimateur des VI dérive
plim_mco = β + ρ*np.sqrt(1-π_faible**2)
ax.axvline(x=plim_mco, color='0.4', linestyle=':', linewidth=1,
           label=r'$\mathrm{plim}\ \hat b_{\mathrm{MCO}}$')

ax.set_xlim(β-2.0, β+2.0)
# Échelle logarithmique : c'est dans les queues que tout se joue
ax.set_yscale('log')
ax.set_ylim(1e-3, 1e1)
ax.set_xlabel(r'$\tilde b_{\mathrm{VI}}$')
ax.set_ylabel('Densité (échelle logarithmique)')
ax.legend(loc='upper left', fontsize='small')
fig.tight_layout()

plt.savefig(PGF / 'instruments-faibles.tex', format='pgf')
