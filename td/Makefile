include ../common.mk

LATEX = pdflatex

all: fiche-exercices.pdf clean

fiche-exercices.pdf: fiche-exercices.tex notations.tex
	@rubber --src-specials --unsafe --pdf fiche-exercices
	@rubber --clean fiche-exercices

# Les éléments de correction sont un document de l'enseignant : la cible est
# volontairement tenue à l'écart de `all`, seule invoquée par l'intégration
# continue (`make -C td`). Ne pas l'ajouter aux prérequis de `all`, ni le PDF
# aux listes `script`/`artifacts` du .gitlab-ci.yml.
correction: correction-exercices.pdf clean

correction-exercices.pdf: correction-exercices.tex notations.tex
	@rubber --src-specials --unsafe --pdf correction-exercices
	@rubber --clean correction-exercices

clean:
	@rm -f $(LATEX_JUNK)
	@rm -rf $(LATEX_JUNK_DIRS)

# fiche-exercices.pdf et correction-exercices.pdf sont produits ici ;
# td-correction-*.pdf sont versionnés et ne doivent pas être supprimés.
clean-all: clean
	@rm -f fiche-exercices.pdf correction-exercices.pdf

.PHONY: all correction clean clean-all
