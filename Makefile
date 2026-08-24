# Makefile racine du cours d'économétrie.
#
#   make            construit les figures engendrées puis tous les documents
#   make figures    régénère seulement les figures dont le script a changé
#   make venv       installe l'environnement virtuel Python
#   make clean      supprime les auxiliaires de tous les répertoires
#
# Les .tex de figures sont versionnés : une compilation des seuls documents
# (`make -C cours`, ce que fait l'intégration continue) n'a pas besoin de
# Python.

include common.mk

# Interpréteur de l'environnement virtuel du dépôt (cf. requirements.txt).
PY = .venv/bin/python3

# Témoin de fraîcheur de l'environnement : « .venv/bin/python3 » est un lien
# symbolique vers l'interpréteur système, qu'on ne peut pas dater soi-même.
VENV = .venv/.stamp

# Un jeu de variables par chapitre ayant des figures engendrées. En ajouter un
# suffit à étendre la chaîne à un nouveau chapitre.
CODES1 = routines/chapitre-1
DATA1  = data/chapitre-1
PGF1   = pgf/chapitre-1

CODES2 = routines/chapitre-2
PGF2   = pgf/chapitre-2

CODES3 = routines/chapitre-3
PGF3   = pgf/chapitre-3

.PHONY: all figures figures-1 figures-2 figures-3 venv cours td examens clean clean-all

all: figures cours td examens

venv: $(VENV)

# ----------------------------------------------------------------------------
# Environnement Python
# ----------------------------------------------------------------------------

$(VENV): requirements.txt
	@echo "Création de l'environnement virtuel Python..."
	@python3 -m venv .venv
	@.venv/bin/pip install --quiet --upgrade pip
	@.venv/bin/pip install --quiet --requirement requirements.txt
	@touch $@

# ----------------------------------------------------------------------------
# Figures engendrées par les scripts Python
#
# Une règle par script. Les scripts qui produisent plusieurs fichiers utilisent
# une cible groupée (« &: »), afin que make ne les lance qu'une seule fois.
# ----------------------------------------------------------------------------

figures: figures-1 figures-2 figures-3

figures-1: $(PGF1)/anscombe.tex \
         $(PGF1)/sample-nonstochastic-x.tex \
         $(PGF1)/slope-estimate-sample-nonstochastic-x.tex \
         $(PGF1)/ols-convergence.tex \
         $(PGF1)/signal-bruit.tex \
         $(PGF1)/gauss-markov.tex \
         $(PGF1)/mco-contraints.tex \
         $(PGF1)/r2-trompeur.tex \
         $(PGF1)/sortie-mincer.tex

$(PGF1)/anscombe.tex: $(CODES1)/anscombe-samples.py $(DATA1)/anscombe.csv $(CODES1)/chemins.py | $(VENV)
	@echo "Les quatre échantillons d'Anscombe..."
	@$(PY) $<

$(PGF1)/sample-nonstochastic-x.tex $(PGF1)/sample-stochastic-x.tex &: \
		$(CODES1)/deterministic-versus-stochastic-samples.py $(CODES1)/chemins.py | $(VENV)
	@echo "Échantillons à exogène déterministe ou stochastique..."
	@$(PY) $<

$(PGF1)/slope-estimate-sample-nonstochastic-x.tex $(PGF1)/slope-estimate-sample-stochastic-x.tex &: \
		$(CODES1)/estimator-with-deterministic-versus-stochastic-samples.py $(CODES1)/chemins.py | $(VENV)
	@echo "Distribution de la pente estimée (100000 échantillons)..."
	@$(PY) $<

$(PGF1)/ols-convergence.tex: $(CODES1)/ols-convergence.py $(CODES1)/chemins.py | $(VENV)
	@echo "Convergence de l'estimateur des MCO (100000 échantillons)..."
	@$(PY) $<

$(PGF1)/signal-bruit.tex: $(CODES1)/signal-bruit.py $(CODES1)/chemins.py | $(VENV)
	@echo "Signal contre bruit..."
	@$(PY) $<

$(PGF1)/gauss-markov.tex: $(CODES1)/gauss-markov.py $(CODES1)/chemins.py | $(VENV)
	@echo "Gauss-Markov contre l'estimateur en deux points..."
	@$(PY) $<

$(PGF1)/mco-contraints.tex: $(CODES1)/mco-contraints.py $(CODES1)/chemins.py | $(VENV)
	@echo "MCO contraints : variance contre biais..."
	@$(PY) $<

$(PGF1)/r2-trompeur.tex: $(CODES1)/r2-trompeur.py $(CODES1)/chemins.py | $(VENV)
	@echo "Ce que le coefficient de détermination ne dit pas..."
	@$(PY) $<

$(PGF1)/sortie-mincer.tex $(PGF1)/sortie-mincer-synthese.tex &: \
		$(CODES1)/mincer.py $(DATA1)/wage1.csv $(CODES1)/chemins.py | $(VENV)
	@echo "Estimation de l'équation de salaire..."
	@$(PY) $<

# ----------------------------------------------------------------------------
# Figures du chapitre 2
# ----------------------------------------------------------------------------

figures-2: $(PGF2)/biais-variable-omise.tex \
           $(PGF2)/erreurs-non-spheriques.tex \
           $(PGF2)/mcg-vs-mco.tex \
           $(PGF2)/normalite-asymptotique-bhat.tex \
           $(PGF2)/tcl.tex

$(PGF2)/biais-variable-omise.tex: $(CODES2)/biais-variable-omise.py $(CODES2)/chemins.py | $(VENV)
	@echo "Biais de variable omise selon la corrélation des régresseurs..."
	@$(PY) $<

$(PGF2)/erreurs-non-spheriques.tex: $(CODES2)/erreurs-non-spheriques.py $(CODES2)/chemins.py | $(VENV)
	@echo "Erreurs sphériques, hétéroscédastiques, autocorrélées..."
	@$(PY) $<

$(PGF2)/mcg-vs-mco.tex: $(CODES2)/mcg-vs-mco.py $(CODES2)/chemins.py | $(VENV)
	@echo "MCG contre MCO sous hétéroscédasticité..."
	@$(PY) $<

$(PGF2)/normalite-asymptotique-bhat.tex: $(CODES2)/normalite-asymptotique-bhat.py $(CODES2)/chemins.py | $(VENV)
	@echo "Normalité asymptotique de b̂ sous erreurs non normales..."
	@$(PY) $<

$(PGF2)/tcl.tex: $(CODES2)/tcl.py $(CODES2)/chemins.py | $(VENV)
	@echo "Théorème central limite..."
	@$(PY) $<

# ----------------------------------------------------------------------------
# Figures du chapitre 3
# ----------------------------------------------------------------------------

figures-3: $(PGF3)/attenuation-erreur-mesure.tex \
           $(PGF3)/simultaneite-offre-demande.tex \
           $(PGF3)/vi-vs-mco.tex \
           $(PGF3)/instruments-faibles.tex \
           $(PGF3)/mco-convergent-ar1.tex

$(PGF3)/attenuation-erreur-mesure.tex: $(CODES3)/attenuation-erreur-mesure.py $(CODES3)/chemins.py | $(VENV)
	@echo "Biais d'atténuation dû à l'erreur de mesure..."
	@$(PY) $<

$(PGF3)/simultaneite-offre-demande.tex: $(CODES3)/simultaneite-offre-demande.py $(CODES3)/chemins.py | $(VENV)
	@echo "Ce que les MCO estiment sur un marché à l'équilibre..."
	@$(PY) $<

$(PGF3)/vi-vs-mco.tex: $(CODES3)/vi-vs-mco.py $(CODES3)/chemins.py | $(VENV)
	@echo "Variables instrumentales contre MCO : le prix de la convergence..."
	@$(PY) $<

$(PGF3)/instruments-faibles.tex: $(CODES3)/instruments-faibles.py $(CODES3)/chemins.py | $(VENV)
	@echo "Ce que devient l'estimateur des VI quand l'instrument est faible..."
	@$(PY) $<

$(PGF3)/mco-convergent-ar1.tex: $(CODES3)/mco-convergent-ar1.py $(CODES3)/chemins.py | $(VENV)
	@echo "MCO biaisés mais convergents dans l'AR(1)..."
	@$(PY) $<

# ----------------------------------------------------------------------------
# Documents
# ----------------------------------------------------------------------------

cours:
	$(MAKE) -C cours all

td:
	$(MAKE) -C td all

examens:
	$(MAKE) -C examens all

# ----------------------------------------------------------------------------
# Nettoyage
# ----------------------------------------------------------------------------

clean:
	$(MAKE) -C cours clean
	$(MAKE) -C td clean
	$(MAKE) -C examens clean
	@rm -rf $(LATEX_JUNK_DIRS) routines/*/__pycache__

clean-all:
	$(MAKE) -C cours clean-all
	$(MAKE) -C td clean-all
	$(MAKE) -C examens clean-all
	@rm -rf $(LATEX_JUNK_DIRS) routines/*/__pycache__ .venv
