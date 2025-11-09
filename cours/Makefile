LATEX = pdflatex

all: chapitre-1.pdf chapitre-2.pdf chapitre-3.pdf chapitre-4.pdf clean

codes/chapitre-1.log: codes/chapitre-1.org
	cd codes ; ./babel chapitre-1.org

chapitre-1.pdf: chapitre-1.tex codes/chapitre-1.log
	@rubber --src-specials --unsafe --pdf chapitre-1
	@rubber --clean chapitre-1

chapitre-2.pdf: chapitre-2.tex
	@rubber --src-specials --unsafe --pdf chapitre-2
	@rubber --clean chapitre-2

chapitre-3.pdf: chapitre-3.tex
	@rubber --src-specials --unsafe --pdf chapitre-3
	@rubber --clean chapitre-3

chapitre-4.pdf: chapitre-4.tex
	@rubber --src-specials --unsafe --pdf chapitre-4
	@rubber --clean chapitre-4

clean:
	@rm -f *.aux *.log *.out *.nav *.rel *.toc *.snm *.synctex.gz *.vrb *.rubbercache
	@rm -rf auto

clean-all:
	@rm -f *.pdf

.PHONY: all
