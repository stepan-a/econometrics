LATEX = pdflatex

all: fiche-exercices.pdf clean

fiche-exercices.pdf: fiche-exercices.tex
	@rubber --src-specials --unsafe --pdf fiche-exercices
	@rubber --clean fiche-exercices

clean:
	@rm -f *.aux *.log *.out *.nav *.rel *.toc *.snm *.synctex.gz *.vrb *.rubbercache
	@rm -rf auto

clean-all: clean
	@rm -f fiche-exercice.pdf

.PHONY: all clean clean-all
