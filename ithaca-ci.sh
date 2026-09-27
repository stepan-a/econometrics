#!/bin/bash
set -e

TARGET="/puck/www/le-mans.adjemian.eu/econometrics"

# --- Build ---------------------------------------------------------------
make -C cours
make -C td
make -C examens

# --- Déploiement des PDF ---------------------------------------------------
install -d -m 0755 "$TARGET"
install -d -m 0755 "$TARGET/codes"

cp cours/chapitre-1.pdf "$TARGET/"
cp cours/chapitre-2.pdf "$TARGET/"
cp cours/chapitre-3.pdf "$TARGET/"
cp cours/chapitre-4.pdf "$TARGET/"

cp examens/partiel-2023.pdf "$TARGET/"
cp examens/partiel-2024.pdf "$TARGET/"
cp examens/partiel-2025.pdf "$TARGET/"
cp examens/rattrapage-2026.pdf "$TARGET/"
cp examens/correction-2023.pdf "$TARGET/"
cp examens/correction-2024.pdf "$TARGET/"
cp examens/correction-2025.pdf "$TARGET/"
cp examens/correction-rattrapage-2026.pdf "$TARGET/"

cp td/fiche-exercices.pdf "$TARGET/"

cp -r routines/chapitre-1 "$TARGET/codes/"
cp -r routines/chapitre-2 "$TARGET/codes/"
cp -r routines/chapitre-3 "$TARGET/codes/"
cp -r routines/chapitre-4 "$TARGET/codes/"

cp -r pgf "$TARGET/"
cp -r tikz "$TARGET/"
cp -r data "$TARGET/"

echo "Déployé sur $TARGET"
