import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2211)

T = 400                            # Taille de l'échantillon
b0, b1 = 1.0, 0.5                  # Vraies valeurs des paramètres

x = 10*rng.uniform(size=T)
a2 = (b1*np.std(x))**2             # Part de variance imputable au signal

fig, axes = plt.subplots(1, 2)

for ax, R2 in zip(axes, [0.10, 0.90]):
    σ = np.sqrt(a2*(1-R2)/R2)      # Écart-type des perturbations donnant ce R²
    y = b0 + b1*x + σ*rng.standard_normal(T)
    xc, yc = x-np.mean(x), y-np.mean(y)
    pente = np.dot(yc, xc)/np.dot(xc, xc)
    constante = np.mean(y) - pente*np.mean(x)
    résidus = y - constante - pente*x
    s2 = np.dot(résidus, résidus)/(T-2)
    t = pente/np.sqrt(s2/np.dot(xc, xc))
    r2 = 1 - np.dot(résidus, résidus)/np.dot(yc, yc)

    ax.scatter(x, y, marker='o', facecolors='none', edgecolor='black', s=11)
    grille = np.array([0.0, 10.0])
    ax.plot(grille, constante + pente*grille, 'r-',
            label=f"$\\hat b_1$ = {pente:.2f} ($t$ = {t:.1f})")
    ax.set_title(f"$R^2$ = {r2:.2f}", fontsize='medium')
    ax.set_xlabel('x')
    ax.legend(loc='upper left', fontsize='small')

axes[0].set_ylabel('y')
fig.tight_layout()

plt.savefig('../images/chapitre-1/r2-trompeur.tex', format='pgf')

