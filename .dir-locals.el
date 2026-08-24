;;; Réglages Emacs locaux au dépôt.  -*- mode: emacs-lisp -*-
;;
;; Placé à la racine, ce fichier couvre aussi bien routines/ (les scripts qui
;; engendrent les figures du cours) qu'exercices/ (les scripts des TD).
;;
;; L'interpréteur Python est celui de l'environnement virtuel du dépôt,
;; installé par `make venv`. Le chemin est calculé à l'ouverture du fichier
;; plutôt qu'écrit en dur, afin de rester valable sur une autre machine et
;; dans un autre répertoire de travail.
;;
;; Emacs demande une confirmation la première fois qu'il évalue le `eval`
;; ci-dessous ; répondre « ! » la mémorise une fois pour toutes.

((python-base-mode
  . ((eval . (let ((racine (locate-dominating-file default-directory ".venv")))
               (when racine
                 (setq-local python-shell-interpreter
                             (expand-file-name ".venv/bin/python3" racine))))))))
