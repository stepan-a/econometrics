import numpy as np

rng = np.random.default_rng(2211)

N = 100000                         # Nombre d'échantillons
T = 10                             # Taille de chaque échantillon

def y(x, ε):
    return x+ε

xd = 10*rng.uniform(size=T)        # Variable exogène déterminsite (utilisée pour YD)

ϵ = rng.normal(size=(T,N))         # Tableau où seront stockés les résidus pour les N échantillons

Bd = np.zeros(N)
Bs = np.zeros(N)

for i in range(N):
    yd = y(xd, ϵ[:,i])
    Bd[i] = np.dot(yd-np.mean(yd), xd-np.mean(xd))/np.dot(xd-np.mean(xd), xd-np.mean(xd))
    xs = 10*rng.uniform(size=T)
    ys = y(xs, ϵ[:,i])
    Bs[i] = np.dot(ys-np.mean(ys), xs-np.mean(xs))/np.dot(xs-np.mean(xs), xs-np.mean(xs))

import matplotlib.pyplot as plt

#
# Histogramme pour la distribution empirique de l'estimateur de la pente quand la variable exogène
# est déterministe.
#

fig, ax = plt.subplots()
ax.hist(Bd, bins='auto', density=True, histtype='step')
#ax.plot(Bd, 0*Bd, marker='o')
plt.savefig('../images/chapitre-1/slope-estimate-sample-nonstochastic-x.tex', format='pgf')

#
# Histogramme pour la distribution empirique de l'estimateur de la pente quand la variable exogène
# est stochastique.
#

fig, ax = plt.subplots()
ax.hist(Bs, bins='auto', density=True, histtype='step')
#ax.plot(Bs, 0*Bd, 'o')
plt.savefig('../images/chapitre-1/slope-estimate-sample-stochastic-x.tex', format='pgf')
