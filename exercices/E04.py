import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Fonction de simulation pour un modèle probit
def simulate(n):
    np.random.seed(42)
    X = np.zeros((n,3))
    X[:,0] = np.random.normal(n)  # Deux variables exogènes continues
    X[:,1] = np.random.normal(n)  # Deux variables exogènes continues
    X[:,2] = np.random.binomial(1, .3, n)
    beta_true = np.array([1, -1, .2])      # Vraies valeurs des Coefficients
    latent = X @ beta_true + np.random.normal(size=n)  # Variable latente
    Y = (latent > 0).astype(int)       # Variable observée (on doit convertir une variable booléenne en entier)
    return Y, X

def estimate_probit(Y, X):
    X = sm.add_constant(X)
    model = sm.Probit(Y, X)
    return model.fit()

def estimate_logit(Y, X):
    X = sm.add_constant(X)
    model = sm.Logit(Y, X)
    return model.fit()

MAX_NOBS = 10000

# Tailles d'échantillons considérées
SampleSizes = np.arange(100, MAX_NOBS, 100, dtype=int)

# Pré-allocation d'un vecteur pour stocker les valeurs de l'estimateur de β₁
β0 = np.zeros(SampleSizes.shape[0])
β1 = np.zeros(SampleSizes.shape[0])
β2 = np.zeros(SampleSizes.shape[0])

for i in range(SampleSizes.shape[0]):
    # On génère des valeurs pour la variable explicative, en supposant que celle-ci est uniformément distribuées
    Sample = simulate(SampleSizes[i])
    Y = Sample[0]
    X = Sample[1]
    results = estimate_probit(Y, X)
    β0[i] = results.params[0]
    β1[i] = results.params[1]
    β2[i] = results.params[2]

    
# Tracé des résultats
plt.figure(figsize=(10,5))
plt.plot(SampleSizes, β1, label=r'$\hat{\beta}_1$')
plt.plot(SampleSizes, β2, label=r'$\hat{\beta}_2$')
plt.axhline(1, linestyle='--', color='black', alpha=0.6)
plt.axhline(-1, linestyle='--', color='black', alpha=0.6)
plt.xlabel("Taille de l'échantillon")
plt.ylabel("Estimation des coefficients")
plt.legend()
plt.title("Modèle Probit")
plt.show()
