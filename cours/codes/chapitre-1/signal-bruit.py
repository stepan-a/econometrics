import numpy as np
import matplotlib.pyplot as plt
from chemins import IMAGES

rng = np.random.default_rng(2211)

N = 60                             # Nombre d'échantillons représentés
T = 25                             # Taille de chaque échantillon
b0, b1 = 1.0, 0.5                  # Vraies valeurs des paramètres
σ = 2.0                            # Écart-type des perturbations

grille = np.array([0.0, 10.0])     # Grille pour tracer les droites estimées

fig, axes = plt.subplots(1, 2, sharey=True, sharex=True)

for ax, sx, titre in zip(axes, [0.7, 2.8],
                         ['Faible variabilité de $x$', 'Forte variabilité de $x$']):
    x = 5.0 + sx*rng.standard_normal(T)          # Même moyenne, dispersion différente
    for i in range(N):
        ϵ = σ*rng.standard_normal(T)
        y = b0 + b1*x + ϵ
        pente = np.dot(y-np.mean(y), x-np.mean(x))/np.dot(x-np.mean(x), x-np.mean(x))
        constante = np.mean(y) - pente*np.mean(x)
        ax.plot(grille, constante + pente*grille, color='gray', alpha=0.35, linewidth=.6)
    ax.plot(grille, b0 + b1*grille, 'r-', linewidth=2, label='Modèle de la nature')
    ax.scatter(x, b0 + b1*x + σ*rng.standard_normal(T),
               marker='o', facecolors='none', edgecolor='black', s=18)
    ax.set_title(titre, fontsize='medium')
    ax.set_xlabel('x')
    ax.set_xlim(0, 10)
    ax.set_ylim(-4, 12)

axes[0].set_ylabel('y')
axes[0].legend(loc='upper left', fontsize='small')
fig.tight_layout()

plt.savefig(IMAGES / 'signal-bruit.tex', format='pgf')

