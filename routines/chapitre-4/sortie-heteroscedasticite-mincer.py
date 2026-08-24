"""L'équation de salaire, revisitée sous hétéroscédasticité.

Reprend l'équation de Mincer estimée au chapitre 1 sur wage1.csv, et met en
regard les écarts-types usuels, HC1 et HC3, puis les statistiques des tests
d'hétéroscédasticité. La régression auxiliaire de White est ici rendue
singulière par la présence simultanée d'exper et d'exper²/100 : on l'estime
donc sur les régresseurs non redondants, et le nombre de degrés de liberté
imprimé est celui du rang effectif.

Produit sortie-mincer-robuste.tex et sortie-mincer-tests.tex.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
from scipy.stats import chi2

from chemins import DONNEES, PGF

data = pd.read_csv(DONNEES / 'wage1.csv')

data['lwage'] = np.log(data.wage)      # Salaire horaire en logarithme
data['exper2'] = data.exper**2/100     # Expérience au carré, en centaines

X = sm.add_constant(data[['educ', 'exper', 'exper2']])
ols = sm.OLS(data.lwage, X).fit()
hc1 = ols.get_robustcov_results(cov_type='HC1')
hc3 = ols.get_robustcov_results(cov_type='HC3')

T = int(ols.nobs)
K = len(ols.params)
cles = ['const', 'educ', 'exper', 'exper2']
noms = {'const': 'Constante',
        'educ': r"$educ$",
        'exper': r"$exper$",
        'exper2': r"$exper^2/100$"}

lignes = []
for i, k in enumerate(cles):
    lignes.append('%s & %.4f & %.4f & %.4f & %.4f & %.2f & %.2f\\\\' %
                  (noms[k], ols.params[k], ols.bse[k], hc1.bse[i], hc3.bse[i],
                   ols.tvalues[k], hc3.tvalues[i]))

tableau = r"""\begin{tabular}{l d d d d d d}
\toprule
 & \multicolumn{1}{c}{$\hat{\mathbf b}_k$}
 & \multicolumn{3}{c}{Écart-type estimé}
 & \multicolumn{2}{c}{Student}\\
\cmidrule(lr){3-5}\cmidrule(lr){6-7}
 &
 & \multicolumn{1}{c}{usuel}
 & \multicolumn{1}{c}{HC1}
 & \multicolumn{1}{c}{HC3}
 & \multicolumn{1}{c}{usuel}
 & \multicolumn{1}{c}{HC3}\\
\midrule
%s
\bottomrule
\end{tabular}""" % ('\n'.join(lignes))

# --- Tests d'hétéroscédasticité ---------------------------------------------

koenker, p_koenker, _, _ = het_breuschpagan(ols.resid, X)
ddl_bp = K - 1

# Statistique originale de Breusch-Pagan : SCE/2 de la régression de ê²/σ̂²
# sur les régresseurs, avec σ̂² l'estimateur du maximum de vraisemblance.
e2 = ols.resid.values**2
g = e2/e2.mean()
aux = sm.OLS(g, X).fit()
bp1979 = ((aux.fittedvalues - g.mean())**2).sum()/2
p_bp1979 = chi2.sf(bp1979, ddl_bp)

# White : la régression auxiliaire complète est singulière (exper² est déjà un
# régresseur). On retient les colonnes de rang plein.
white, p_white, _, _ = het_white(ols.resid, X)
ddl_white = int(np.linalg.matrix_rank(
    np.column_stack([X.values[:, 1:],
                     X.values[:, 1:]**2,
                     X.educ*X.exper, X.educ*X.exper2, X.exper*X.exper2])))

def pval(p):
    """p-value à la française, tronquée sous le millième."""
    return r'$<10^{-3}$' if p < 1e-3 else ('%.4f' % p).replace('.', '{,}')


tests = (r"""\begin{tabular}{l d c c}
\toprule
 & \multicolumn{1}{c}{Statistique}
 & Degrés de liberté
 & p-value\\
\midrule
Breusch-Pagan (1979) & %.2f & %d & %s\\
Breusch-Pagan studentisé (Koenker) & %.2f & %d & %s\\
White & %.2f & %d & %s\\
\bottomrule
\end{tabular}""" % (bp1979, ddl_bp, pval(p_bp1979),
                    koenker, ddl_bp, pval(p_koenker),
                    white, ddl_white, pval(p_white)))

with open(PGF / 'sortie-mincer-robuste.tex', 'w') as f:
    f.write(tableau + '\n')

with open(PGF / 'sortie-mincer-tests.tex', 'w') as f:
    f.write(tests + '\n')

print('T = %d, K = %d' % (T, K))
for i, k in enumerate(cles):
    print('%-14s b = %8.4f  usuel %.4f  HC1 %.4f  HC3 %.4f  (HC3/usuel = %.2f)'
          % (k, ols.params[k], ols.bse[k], hc1.bse[i], hc3.bse[i],
             hc3.bse[i]/ols.bse[k]))
print('Breusch-Pagan 1979 %.2f (ddl %d, p = %.4f)' % (bp1979, ddl_bp, p_bp1979))
print('Breusch-Pagan Koenker %.2f (ddl %d, p = %.4f)' % (koenker, ddl_bp, p_koenker))
print('White %.2f (ddl %d, p = %.4f)' % (white, ddl_white, p_white))
print('Levier maximal %.3f' % np.max(ols.get_influence().hat_matrix_diag))
