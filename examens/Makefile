all: partiel-2023.pdf correction-2023.pdf partiel-2024.pdf correction-2024.pdf

%.pdf: %.tex
	rubber --pdf $^
	rubber --clean $^

clean-all:
	rm -f partiel-*.pdf
	rm -f correction-*.pdf
	rm -rf auto

.PHONY: clean-all
