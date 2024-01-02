LATEX = pdflatex

all: partiel-2023.pdf correction-2023.pdf clean

partiel-2023.pdf: partiel-2023.tex
	while ($(LATEX) partiel-2023.tex ; \
	grep -q "Rerun to get cross" partiel-2023.log ) do true ; \
	done

correction-2023.pdf: correction-2023.tex
	while ($(LATEX) correction-2023.tex ; \
	grep -q "Rerun to get cross" correction-2023.log ) do true ; \
	done

clean:
	rm -rf *.aux
	rm -rf *.out
	rm -rf auto
	rm -rf *.log
	rm -rf *.synctex.gz

clean-all: clean
	rm -f *.pdf
	rm -f *.tikz
	rm -f *.log
