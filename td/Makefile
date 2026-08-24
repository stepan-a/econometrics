include ../common.mk

LATEX = pdflatex

all: fiche-exercices.pdf clean

fiche-exercices.pdf: fiche-exercices.tex
	@rubber --src-specials --unsafe --pdf fiche-exercices
	@rubber --clean fiche-exercices

clean:
	@rm -f $(LATEX_JUNK)
	@rm -rf $(LATEX_JUNK_DIRS)

# Seul fiche-exercices.pdf est produit ici ; td-correction-*.pdf sont versionnés
# et ne doivent pas être supprimés.
clean-all: clean
	@rm -f fiche-exercices.pdf

.PHONY: all clean clean-all
