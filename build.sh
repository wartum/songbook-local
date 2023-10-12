#!/bin/sh

upload() {
	aws s3 cp songbook.pdf s3://piewoj/songbook.pdf
	aws s3api put-object-tagging --bucket piewoj --key songbook.pdf --tagging 'TagSet={Key=public,Value=yes}'
}

python3 ./python/convert.py
pdflatex -halt-on-error ./songbook.tex > /dev/null
pdflatex -halt-on-error ./songbook.tex > /dev/null

rm ./songbook.aux
rm ./songbook.log
rm ./songbook.out
rm ./songbook.toc

if [ "$1" = "upload" ]; then upload; fi
