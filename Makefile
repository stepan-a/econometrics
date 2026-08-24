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

CODES  = cours/codes/chapitre-1
DATA   = cours/data/chapitre-1
IMAGES = cours/images/chapitre-1

.PHONY: all figures venv cours td examens clean clean-all

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

figures: $(IMAGES)/anscombe.tex \
         $(IMAGES)/sample-nonstochastic-x.tex \
         $(IMAGES)/slope-estimate-sample-nonstochastic-x.tex \
         $(IMAGES)/ols-convergence.tex \
         $(IMAGES)/signal-bruit.tex \
         $(IMAGES)/gauss-markov.tex \
         $(IMAGES)/mco-contraints.tex \
         $(IMAGES)/r2-trompeur.tex \
         $(IMAGES)/sortie-mincer.tex

$(IMAGES)/anscombe.tex: $(CODES)/anscombe-samples.py $(DATA)/anscombe.csv $(CODES)/chemins.py | $(VENV)
	@echo "Les quatre échantillons d'Anscombe..."
	@$(PY) $<

$(IMAGES)/sample-nonstochastic-x.tex $(IMAGES)/sample-stochastic-x.tex &: \
		$(CODES)/deterministic-versus-stochastic-samples.py $(CODES)/chemins.py | $(VENV)
	@echo "Échantillons à exogène déterministe ou stochastique..."
	@$(PY) $<

$(IMAGES)/slope-estimate-sample-nonstochastic-x.tex $(IMAGES)/slope-estimate-sample-stochastic-x.tex &: \
		$(CODES)/estimator-with-deterministic-versus-stochastic-samples.py $(CODES)/chemins.py | $(VENV)
	@echo "Distribution de la pente estimée (100000 échantillons)..."
	@$(PY) $<

$(IMAGES)/ols-convergence.tex: $(CODES)/ols-convergence.py $(CODES)/chemins.py | $(VENV)
	@echo "Convergence de l'estimateur des MCO (100000 échantillons)..."
	@$(PY) $<

$(IMAGES)/signal-bruit.tex: $(CODES)/signal-bruit.py $(CODES)/chemins.py | $(VENV)
	@echo "Signal contre bruit..."
	@$(PY) $<

$(IMAGES)/gauss-markov.tex: $(CODES)/gauss-markov.py $(CODES)/chemins.py | $(VENV)
	@echo "Gauss-Markov contre l'estimateur en deux points..."
	@$(PY) $<

$(IMAGES)/mco-contraints.tex: $(CODES)/mco-contraints.py $(CODES)/chemins.py | $(VENV)
	@echo "MCO contraints : variance contre biais..."
	@$(PY) $<

$(IMAGES)/r2-trompeur.tex: $(CODES)/r2-trompeur.py $(CODES)/chemins.py | $(VENV)
	@echo "Ce que le coefficient de détermination ne dit pas..."
	@$(PY) $<

$(IMAGES)/sortie-mincer.tex $(IMAGES)/sortie-mincer-synthese.tex &: \
		$(CODES)/mincer.py $(DATA)/wage1.csv $(CODES)/chemins.py | $(VENV)
	@echo "Estimation de l'équation de salaire..."
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
	@rm -rf $(LATEX_JUNK_DIRS) $(CODES)/__pycache__

clean-all:
	$(MAKE) -C cours clean-all
	$(MAKE) -C td clean-all
	$(MAKE) -C examens clean-all
	@rm -rf $(LATEX_JUNK_DIRS) $(CODES)/__pycache__ .venv
