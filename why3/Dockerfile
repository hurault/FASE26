FROM ocaml/opam:ubuntu-lts

# Installer les dépendances système
RUN sudo apt -y install \
    libgmp-dev linux-libc-dev pkg-config cvc5=1.1.2-1build1 python3 \
    libcairo2-dev libexpat1-dev libgtk-3-dev libgtksourceview-3.0-dev zlib1g-dev

# Créer un switch OCaml
RUN opam switch create 5.3.0
# Mettre à jour l'environnement opam dans le shell
SHELL ["/bin/bash", "-c"]
RUN eval $(opam env) && \
    opam install -y \
      why3.1.8.1 why3-ide.1.8.1 z3.4.15.2 alt-ergo.2.6.2 \
      coq.8.20.1 why3-coq.1.8.1 && \
    why3 config detect

# Copier les fichiers
COPY encoding-ok.mlw .
COPY encoding-ok encoding-ok

# Commande par défaut
CMD ["bash", "-c", "eval $(opam env) && why3 replay encoding-ok"]