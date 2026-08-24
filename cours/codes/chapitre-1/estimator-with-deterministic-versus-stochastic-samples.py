"""Distribution de l'estimateur de la pente, exogène déterministe ou stochastique.

Produit slope-estimate-sample-nonstochastic-x.tex et
slope-estimate-sample-stochastic-x.tex.
"""

import numpy as np
import matplotlib.pyplot as plt

from chemins import IMAGES

rng = np.random.default_rng(2211)

N = 100000                         # Nombre d'échantillons
T = 10                             # Taille de chaque échantillon


def y(x, ε):
    # Le modèle de la nature
    return x+ε


xd = 10*rng.uniform(size=T)        # Variable exogène déterministe

ϵ = rng.normal(size=(T,N))         # Résidus pour les N échantillons

Bd = np.zeros(N)
Bs = np.zeros(N)

for i in range(N):
    yd = y(xd, ϵ[:,i])
    Bd[i] = np.dot(yd-np.mean(yd), xd-np.mean(xd))/np.dot(xd-np.mean(xd), xd-np.mean(xd))
    xs = 10*rng.uniform(size=T)
    ys = y(xs, ϵ[:,i])
    Bs[i] = np.dot(ys-np.mean(ys), xs-np.mean(xs))/np.dot(xs-np.mean(xs), xs-np.mean(xs))

# Distribution empirique de la pente estimée, exogène déterministe

fig, ax = plt.subplots()
ax.hist(Bd, bins='auto', density=True, histtype='step')
plt.savefig(IMAGES / 'slope-estimate-sample-nonstochastic-x.tex', format='pgf')

# Distribution empirique de la pente estimée, exogène stochastique

fig, ax = plt.subplots()
ax.hist(Bs, bins='auto', density=True, histtype='step')
plt.savefig(IMAGES / 'slope-estimate-sample-stochastic-x.tex', format='pgf')
