"""Emplacements de référence, partagés par les scripts du chapitre 4.

Les chemins sont déduits de la position de ce fichier, de sorte que les scripts
s'exécutent indifféremment depuis la racine du dépôt ou depuis leur propre
répertoire.

DONNEES : l'équation de salaire sert de fil rouge depuis le chapitre 1. Les
          données sont celles du chapitre 1, on ne les duplique pas.
PGF     : figures engendrées, incluses par les transparents. Tout ce qui s'y
          trouve est reconstructible par `make figures`.
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
DONNEES = RACINE / 'data' / 'chapitre-1'
PGF = RACINE / 'pgf' / 'chapitre-4'
