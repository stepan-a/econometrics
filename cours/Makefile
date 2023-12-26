LATEX = pdflatex

all: chapitre-1.pdf clean

images/chapitre-1/app-01-sample-nonstochastic-x.tex: codes/chapitre-1/app-001.py
	python3 codes/chapitre-1/app-001.py

images/chapitre-1/app-01-sample-stochastic-x.tex: codes/chapitre-1/app-001.py
	python3 codes/chapitre-1/app-001.py

chapitre-1.pdf: chapitre-1.tex images/chapitre-1/app-01-sample-nonstochastic-x.tex images/chapitre-1/app-01-sample-nonstochastic-x.tex
	@rubber --src-specials --unsafe --pdf chapitre-1

clean:
	@rm -f *.aux *.log *.out *.nav *.rel *.toc *.snm *.synctex.gz *.vrb *.rubbercache
	@rm -rf auto

clean-all:
	@rm -f *.pdf

.PHONY: all
