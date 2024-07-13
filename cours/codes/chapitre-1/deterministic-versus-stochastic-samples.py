import numpy as np

rng = np.random.default_rng(2211)

N = 100                            # Nombre d'échantillons
T = 10                             # Taille de chaque échantillon

def y(x, ε):
    return x+ε

x = 10*rng.uniform(size=(T,1))     # Variable exogène déterminsite (utilisée pour YD)

ϵ = rng.normal(size=(T,N))         # Tableau où seront stockés les résidus pour les N échantillons

YD = np.zeros((T,N))               # N échantillons (pour y) avec variable exogène déterministe
YS = np.zeros((T,N))               # N échantillons (pour y) avec variable exogène stochastique
XS = np.zeros((T,N))               # N échantillons (pour x) avec variable exogène stochastique

for i in range(N):
    YD[:,i] = y(x, ϵ[:,i])[:,0]
    XS[:,i] = 10*rng.uniform(size=(T,1))[:,0]
    YS[:,i] = y(XS[:,i], ϵ[:,i])

import matplotlib.pyplot as plt

#
# Représentation graphique d''échantillons avec variable exogène déterministe
#

fig, ax = plt.subplots()

for i in range(N):
    ax.scatter(x, YD[:,i], marker='o', facecolors='none', edgecolor='black')

plt.savefig('sample-nonstochastic-x.tex', format='pgf')

#
# Représentation graphique d''échantillons avec variable exogène stochastique
#

fig, ax = plt.subplots()

for i in range(N):
    ax.scatter(XS[:,i], YS[:,i], marker='o', facecolors='none', edgecolor='black')

plt.savefig('sample-stochastic-x.tex', format='pgf')

#
# Un peu de ménage
#

from shutil import move

move('sample-nonstochastic-x.tex', '../images/chapitre-1/sample-nonstochastic-x.tex')
move('sample-stochastic-x.tex', '../images/chapitre-1/sample-stochastic-x.tex')
