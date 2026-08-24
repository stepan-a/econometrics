"""Échantillons avec variable exogène déterministe ou stochastique.

Produit sample-nonstochastic-x.tex et sample-stochastic-x.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import IMAGES

rng = np.random.default_rng(2211)

N = 100                            # Nombre d'échantillons
T = 10                             # Taille de chaque échantillon


def y(x, ε):
    # Le modèle de la nature
    return x+ε


x = 10*rng.uniform(size=(T,1))     # Variable exogène déterministe (utilisée pour YD)

ϵ = rng.normal(size=(T,N))         # Résidus pour les N échantillons

YD = np.zeros((T,N))               # N échantillons (pour y) avec variable exogène déterministe
YS = np.zeros((T,N))               # N échantillons (pour y) avec variable exogène stochastique
XS = np.zeros((T,N))               # N échantillons (pour x) avec variable exogène stochastique

for i in range(N):
    YD[:,i] = y(x, ϵ[:,i])[:,0]
    XS[:,i] = 10*rng.uniform(size=(T,1))[:,0]
    YS[:,i] = y(XS[:,i], ϵ[:,i])

# Échantillons avec variable exogène déterministe

fig, ax = plt.subplots()

for i in range(N):
    ax.scatter(x, YD[:,i], marker='o', facecolors='none', edgecolor='black')

plt.savefig(IMAGES / 'sample-nonstochastic-x.tex', format='pgf')

# Échantillons avec variable exogène stochastique

fig, ax = plt.subplots()

for i in range(N):
    ax.scatter(XS[:,i], YS[:,i], marker='o', facecolors='none', edgecolor='black')

plt.savefig(IMAGES / 'sample-stochastic-x.tex', format='pgf')
