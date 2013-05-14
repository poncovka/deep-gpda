#!/usr/bin/bash
# makefile pro vytvoreni zipu pro CD

rm -rf CD
mkdir CD	
cd bakalarka
make final
cp projekt.pdf ../CD/xponco00.pdf
make clean
tar czvf bp-xponco00.tar.gz *.tex *.bib *.bst ./fig/* Makefile Changelog counter.sh *.cls ./img/*.eps ./obsah/*.tex
cp bp-xponco00.tar.gz ../CD/bp.tar.gz
cd ../aplikace
rm -f aplikace-xponco00.tar.gz
tar czvf aplikace-xponco00.tar.gz MANUAL *.py ./example/* ./gdeep_pda/*.py ./test/*.py ./test/input/*
cp aplikace-xponco00.tar.gz ../CD/aplikace.tar.gz
cd ../CD
cp ../README README
mkdir aplikace
mkdir bp
tar xzvf aplikace.tar.gz -C aplikace
tar xzvf bp.tar.gz -C bp
