"""Emplacements de référence, partagés par les scripts du chapitre 2.

Les chemins sont déduits de la position de ce fichier, de sorte que les scripts
s'exécutent indifféremment depuis la racine du dépôt ou depuis leur propre
répertoire.

PGF : figures engendrées, incluses par les transparents. Tout ce qui s'y trouve
      est reconstructible par `make figures`. Les figures du chapitre 2 étant
      toutes simulées, aucun jeu de données n'est nécessaire.
"""

from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
PGF = RACINE / 'pgf' / 'chapitre-2'
