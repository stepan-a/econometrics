import numpy as np
import pandas as pd
import statsmodels.api as sm

data = pd.read_csv('../data/chapitre-1/wage1.csv')

data['lwage']  = np.log(data.wage)     # Salaire horaire en logarithme
data['exper2'] = data.exper**2/100     # Expérience au carré (profil concave), en centaines

X = sm.add_constant(data[['educ', 'exper', 'exper2']])
ols = sm.OLS(data.lwage, X).fit()

T = int(ols.nobs)
K = len(ols.params)

noms = {'const': 'Constante',
        'educ': r"$educ$ (années d'études)",
        'exper': r"$exper$ (années d'expérience)",
        'exper2': r"$exper^2/100$"}

lignes = []
for k in ['const', 'educ', 'exper', 'exper2']:
    lignes.append('%s & %.4f & %.4f & %.2f & %.3f\\\\' %
                  (noms[k], ols.params[k], ols.bse[k], ols.tvalues[k], ols.pvalues[k]))

tableau = r"""\begin{tabular}{l d d d d}
\toprule
 & \multicolumn{1}{c}{$\hat{\mathbf b}_i$}
 & \multicolumn{1}{c}{$s_{\hat{\mathbf b}_i}$}
 & \multicolumn{1}{c}{$t$}
 & \multicolumn{1}{c}{p-value}\\
\midrule
%s
\bottomrule
\end{tabular}""" % ('\n'.join(lignes))

def fr(x, n):
    """Formate un nombre à la française (virgule décimale)."""
    return ('%.*f' % (n, x)).replace('.', ',')

synthese = (r"""\begin{tabular}{ll}
$T = %d$ observations, $K = %d$ paramètres & $R^2 = %s$\\
$s = \sqrt{\nicefrac{SSE}{(T-K)}} = %s$ & $\bar R^2 = %s$\\
$F(%d,\,%d) = %s$ & p-value $< 10^{-3}$\\
\end{tabular}""" %
    (T, K, fr(ols.rsquared, 4), fr(np.sqrt(ols.mse_resid), 4),
     fr(ols.rsquared_adj, 4), K-1, T-K, fr(ols.fvalue, 2)))

with open('../images/chapitre-1/sortie-mincer.tex', 'w') as f:
    f.write(tableau + '\n')

with open('../images/chapitre-1/sortie-mincer-synthese.tex', 'w') as f:
    f.write(synthese + '\n')

