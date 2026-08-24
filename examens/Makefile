include ../common.mk

TEXFILES := $(wildcard *.tex)
PDFS     := $(TEXFILES:.tex=.pdf)

all: $(PDFS)

%.pdf: %.tex
	latexmk -pdf -interaction=nonstopmode -quiet $<
	latexmk -c $<
	rm -f *.synctex.gz

clean:
	@rm -f $(LATEX_JUNK)
	@rm -rf $(LATEX_JUNK_DIRS)

# Ne supprime que les PDF issus d'un .tex de ce répertoire : les documents sans
# source (scans, sujets d'archive) sont préservés.
clean-all: clean
	@rm -f $(PDFS)

# Alias historique.
distclean: clean-all

.PHONY: all clean clean-all distclean
