"""Convergence de l'estimateur des MCO quand la taille de l'échantillon croît.

Produit ols-convergence.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import IMAGES

rng = np.random.default_rng(2211)

N = 100000                         # Nombre d'échantillons


def y(x, ε):
    # Le modèle de la nature
    return x+ε


fig, ax = plt.subplots()

colours = ['b', 'g', 'r']

for t in range(0,3):
    T = 10*10**t
    xd = 10*rng.uniform(size=T)
    B = np.zeros(N)
    for i in range(N):
        ϵ = rng.normal(size=T)
        yd = y(xd, ϵ)
        B[i] = np.dot(yd-np.mean(yd), xd-np.mean(xd))/np.dot(xd-np.mean(xd), xd-np.mean(xd))
    ax.hist(B, bins='auto', density=True, histtype='step', color=colours[t], label=f"T = {T}")

ax.legend()
plt.savefig(IMAGES / 'ols-convergence.tex', format='pgf')
