include ../common.mk

LATEX = pdflatex

all: chapitre-1.pdf chapitre-2.pdf chapitre-3.pdf chapitre-4.pdf clean

codes/chapitre-1.log: codes/chapitre-1.org
	cd codes ; ./babel chapitre-1.org

chapitre-1.pdf: chapitre-1.tex preamble.tex codes/chapitre-1.log
	@rubber --src-specials --unsafe --pdf chapitre-1
	@rubber --clean chapitre-1

chapitre-2.pdf: chapitre-2.tex preamble.tex
	@rubber --src-specials --unsafe --pdf chapitre-2
	@rubber --clean chapitre-2

chapitre-3.pdf: chapitre-3.tex preamble.tex
	@rubber --src-specials --unsafe --pdf chapitre-3
	@rubber --clean chapitre-3

chapitre-4.pdf: chapitre-4.tex preamble.tex
	@rubber --src-specials --unsafe --pdf chapitre-4
	@rubber --clean chapitre-4

clean:
	@rm -f $(LATEX_JUNK)
	@rm -rf $(LATEX_JUNK_DIRS)

# Cache des figures externalisées par tikzexternalize. Le reconstruire coûte une
# dizaine de minutes, d'où une cible distincte de `clean`. Le .gitignore du
# répertoire est préservé.
clean-figures:
	@rm -f figures/chapitre-*-figure*

clean-all: clean clean-figures
	@rm -f *.pdf

.PHONY: all clean clean-figures clean-all
