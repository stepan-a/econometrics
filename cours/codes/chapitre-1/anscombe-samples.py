import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def plot(ax, x, y, title=''):
  """
  Représente y contre x, ainsi que la droite de régression
  """

  assert np.shape(x) == np.shape(y), "Données pour x et y incompatibles."

  regression = stats.linregress(x, y)


  # Données et coefficient de détermination
  ax.scatter(x, y,  marker='o', facecolors='none', edgecolor='black')#, label=f"R^2 = {regression.rvalue**2:.2f}")

  # Linear regression
  xx = np.array([0, 20])
  yy = regression.slope * xx + regression.intercept
  ax.plot(xx, yy, 'r-', label=f"y = {regression.slope:.2f} x + {regression.intercept:.2f}")

  # Légende
  leg = ax.legend(loc='upper left', fontsize='small')

  # Titre
  if title:
    ax.set_title(title)

  subplot = ax.get_subplotspec()

  if subplot.is_last_row():
    ax.set_xlabel("x")

  if subplot.is_first_col():
    ax.set_ylabel("y")

  return regression


fig = plt.figure()

# Lecture des quatre échantillons
data = pd.read_csv('../data/chapitre-1/anscombe.csv')

ax = fig.add_subplot(2, 2, 1)
x = data[data.dataset=='I'].x
y = data[data.dataset=='I'].y
plot(ax, x, y, title=f'I')

ax = fig.add_subplot(2, 2, 2)
x = data[data.dataset=='II'].x
y = data[data.dataset=='II'].y
plot(ax, x, y, title=f'II')

ax = fig.add_subplot(2, 2, 3)
x = data[data.dataset=='III'].x
y = data[data.dataset=='III'].y
plot(ax, x, y, title=f'III')

ax = fig.add_subplot(2, 2, 4)
x = data[data.dataset=='IV'].x
y = data[data.dataset=='IV'].y
regression = plot(ax, x, y, title=f'IV')

# fig.suptitle(f"Les quatre échantillons d'Anscombe ($R^2 = {regression.rvalue**2:.2f}$)", fontsize='x-large')
fig.tight_layout()

plt.savefig('../images/chapitre-1/anscombe.tex', format='pgf')
