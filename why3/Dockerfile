FROM ocaml/opam:ubuntu-lts

RUN sudo apt -y install libgmp-dev linux-libc-dev pkg-config cvc5=1.1.2-1build1 python3 libcairo2-dev libexpat1-dev libgtk-3-dev libgtksourceview-3.0-dev zlib1g-dev

RUN opam switch create 5.3.0

RUN eval $(opam env)

RUN opam install -y why3.1.8.1 why3-ide.1.8.1 z3.4.15.2 alt-ergo.2.6.2 coq.8.20.1 why3-coq.1.8.1

RUN eval $(opam env) && why3 config detect

COPY encoding-ok.mlw .

COPY encoding-ok encoding-ok

CMD ["why3", "ide", "encoding-ok.mlw"]
#CMD ["why3","replay","encoding-ok"]
