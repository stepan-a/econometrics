"""Emplacements de référence, partagés par les scripts du chapitre 1.

Les chemins sont déduits de la position de ce fichier, de sorte que les scripts
s'exécutent indifféremment depuis la racine du dépôt, depuis cours/ ou depuis
leur propre répertoire.
"""

from pathlib import Path

COURS = Path(__file__).resolve().parents[2]
DONNEES = COURS / 'data' / 'chapitre-1'
IMAGES = COURS / 'images' / 'chapitre-1'
