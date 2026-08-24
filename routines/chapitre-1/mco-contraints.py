import numpy as np
import matplotlib.pyplot as plt
from chemins import PGF

rng = np.random.default_rng(2211)

N = 20000                          # Nombre d'échantillons
T = 40                             # Taille de chaque échantillon
σ = 1.0                            # Écart-type des perturbations

# Deux régresseurs négativement corrélés (déterministes), plus une constante.
# C'est alors la somme β2 + β3 qui est mal identifiée : la contraindre est très
# informatif. Avec des régresseurs positivement corrélés, le gain serait minime.
z = rng.standard_normal(T)
x1 = z + 0.4*rng.standard_normal(T)
x2 = -z + 0.4*rng.standard_normal(T)
X = np.column_stack([np.ones(T), x1, x2])

XX = X.T @ X
XXi = np.linalg.inv(XX)
R = np.array([[0.0, 1.0, 1.0]])    # On contraint β2 + β3
r = np.array([1.0])
A = XXi @ R.T @ np.linalg.inv(R @ XXi @ R.T)   # Matrice de correction

fig, axes = plt.subplots(1, 2, sharex=True)

scénarios = [(np.array([0.5, 0.6, 0.4]), 'Contrainte vraie ($\\beta_2+\\beta_3=1$)'),
             (np.array([0.5, 0.6, 0.9]), 'Contrainte fausse ($\\beta_2+\\beta_3=1,5$)')]

for ax, (β, titre) in zip(axes, scénarios):
    Bh = np.zeros(N)               # MCO non contraints
    Bt = np.zeros(N)               # MCO contraints
    for i in range(N):
        y = X @ β + σ*rng.standard_normal(T)
        bh = XXi @ (X.T @ y)
        bt = bh - A @ (R @ bh - r)
        Bh[i] = bh[1]
        Bt[i] = bt[1]
    ax.hist(Bh, bins='auto', density=True, histtype='step', color='b',
            label=f"$\\hat b_2$ (écart-type {np.std(Bh):.3f})")
    ax.hist(Bt, bins='auto', density=True, histtype='step', color='g',
            label=f"$\\tilde b_2$ (écart-type {np.std(Bt):.3f})")
    ax.axvline(x=β[1], color='r', linestyle='--', linewidth=1,
               label='Vraie valeur $\\beta_2$')
    ax.set_title(titre, fontsize='medium')
    ax.set_xlabel(r'$b_2$')
    ax.legend(loc='upper left', fontsize='small')

axes[0].set_ylabel('Densité')
fig.tight_layout()

plt.savefig(PGF / 'mco-contraints.tex', format='pgf')

