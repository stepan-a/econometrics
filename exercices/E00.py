import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Les valeurs (vraies) des paramètres du modèle linéaire simple
beta0 = 2  # Intercept
beta1 = 3  # Slope
sigma = 1  # Écart-type de l'erreur

MAX_NOBS = 100000

# Tailles d'échantillons considérées
sample_sizes = np.arange(10, MAX_NOBS, 1000, dtype=int)

# Pré-allocation d'un vecteur pour stocker les valeurs de l'estimateur de β₁
beta1_estimates = np.zeros(sample_sizes.shape[0])

for i in range(sample_sizes.shape[0]):
    # On génère des valeurs pour la variable explicative, en supposant que celle-ci est uniformément distribuées
    x = np.random.uniform(0, 10, sample_sizes[i])
    # On génère des erreurs normalement distribées
    epsilon = np.random.normal(0, sigma, sample_sizes[i])
    # On consruit la variable endogène
    y = beta0 + beta1 * x + epsilon
    # On définit la matrice des exogènes 
    X = sm.add_constant(x)
    # Estimation par les MCO
    model = sm.OLS(y, X).fit()
    # On sauvegarde la valeur de l'estimateur de β₁
    beta1_estimates[i] = model.params[1]

# Tracer la convergence
plt.figure(figsize=(8,5))
plt.plot(sample_sizes, beta1_estimates, label="Estimation Monte-Carlo", marker='o', linewidth=0) # linewidth=0 pour virer les droites entre les points
plt.axhline(y=beta1, color='r', linestyle='--', label="Vraie valeur de $\\beta_1$")
plt.xlabel("Taille de l'échantillon")
plt.ylabel("Estimation de $\\beta_1$")
plt.title("Convergence de l'estimateur MCO par Monte-Carlo")
plt.legend()
plt.grid()
plt.show()
