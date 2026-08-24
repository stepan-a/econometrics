# -*- mode: makefile -*-
#
# Réglages communs aux Makefile de cours/, td/ et examens/.
#
# Chaque Makefile charge ce fichier par `include ../common.mk`, puis définit ses
# cibles `clean` et `clean-all` à partir des variables ci-dessous. La liste suit
# celle du .gitignore, augmentée des résidus que rubber, latexmk, minted et
# AUCTeX laissent derrière eux.

# Auxiliaires LaTeX, biblatex/biber, Beamer, tikzexternalize, latexmk.
# `git.hash` est produit par le \write18 du préambule (cours/ uniquement) ;
# le supprimer ailleurs est sans effet.
LATEX_JUNK = *.aux *.auxlock *.bbl *.bcf *.blg *.fdb_latexmk *.fls *.log \
             *.nav *.out *.rel *.run.xml *.snm *.synctex.gz \
             *.synctex\(busy\) *.toc *.vrb *.rubbercache git.hash

# Répertoires laissés par minted, AUCTeX et rubber.
LATEX_JUNK_DIRS = auto .ltx .auctex-auto _minted _minted-*
