#!/bin/sh

python3 ./python/convert.py
pdflatex -halt-on-error ./songbook.tex > /dev/null
pdflatex -halt-on-error ./songbook.tex > /dev/null

rm ./songbook.aux
rm ./songbook.log
rm ./songbook.out
rm ./songbook.toc
