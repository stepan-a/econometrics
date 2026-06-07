import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Condition initiale du générateur de nombre aléatoires (seed)
rng = np.random.default_rng(2211)

N = 100000                         # Nombre d'échantillons

T = 100                            # Nombre d'observations dans chaque séries temporelles

B = np.zeros(N)
S = np.zeros(N)
R = np.zeros(N)

for i in range(N):
    # Simulation de deux marches aléatoires indépendantes
y = np.cumsum(rng.normal(size=T))
x = np.cumsum(rng.normal(size=T))
X = sm.add_constant(x)
# Estimation du modèle yₜ = a + bxₜ +uₜ
model = sm.OLS(y, X).fit()
    # On sauvegarde la valeur de l'estimateur de β₁
    beta1_estimates[i] = model.params[1]
    
    yd = y(xd, ϵ)
    B[i] = np.dot(yd-np.mean(yd), xd-np.mean(xd))/np.dot(xd-np.mean(xd), xd-np.mean(xd))
    ax.hist(B, bins='auto', density=True, histtype='step', color=colours[t], label=f"T = {T}")

ax.legend()
plt.show()
