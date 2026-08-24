import numpy as np
import matplotlib.pyplot as plt
from chemins import IMAGES

rng = np.random.default_rng(2211)

N = 50000                          # Nombre d'échantillons
T = 20                             # Taille de chaque échantillon
b0, b1 = 1.0, 1.0                  # Vraies valeurs des paramètres

x = 10*rng.uniform(size=T)         # Variable exogène déterministe
haut = x > np.median(x)            # Partition de l'échantillon en deux moitiés
bas = ~haut
écart_x = np.mean(x[haut]) - np.mean(x[bas])

B_mco = np.zeros(N)                # Estimateur des MCO
B_2pt = np.zeros(N)                # Estimateur « en deux points »

xc = x - np.mean(x)

for i in range(N):
    ϵ = rng.normal(size=T)
    y = b0 + b1*x + ϵ
    B_mco[i] = np.dot(y-np.mean(y), xc)/np.dot(xc, xc)
    B_2pt[i] = (np.mean(y[haut]) - np.mean(y[bas]))/écart_x

fig, ax = plt.subplots()
ax.hist(B_2pt, bins='auto', density=True, histtype='step', color='g',
        label=f"Deux points (écart-type {np.std(B_2pt):.3f})")
ax.hist(B_mco, bins='auto', density=True, histtype='step', color='b',
        label=f"MCO (écart-type {np.std(B_mco):.3f})")
ax.axvline(x=b1, color='r', linestyle='--', linewidth=1,
           label='Vraie valeur de la pente')
ax.set_xlabel(r'$\hat b_1$')
ax.set_ylabel('Densité')
ax.legend(loc='upper left', fontsize='small')
fig.tight_layout()

plt.savefig(IMAGES / 'gauss-markov.tex', format='pgf')

