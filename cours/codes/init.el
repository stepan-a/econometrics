(org-babel-do-load-languages
 'org-babel-load-languages
 '(
   (emacs-lisp . t)
   (org . t)
   (latex . t)
   (shell . t)
   (python . t)
   (gnuplot . t)
   (matlab . t)
   (R . t)
   (lilypond . t)
   ))

(setq org-src-fontify-natively t)
(setq org-src-tab-acts-natively t)
(setq org-babel-python-command "python3")
(setq org-html-htmlize-output-type 'css)
(setq org-html-head-include-default-style nil)
(setq org-confirm-babel-evaluate nil)
