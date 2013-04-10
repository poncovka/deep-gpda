# makefile pro preklad LaTeX verze Bc. prace
# (c) 2008 Michal Bidlo
# E-mail: bidlom AT fit vutbr cz
#===========================================
# asi budete chtit prejmenovat:
CO=projekt
OBSAH=obsah
REF=literatura

all: clean $(CO).ps

final: clean $(CO).pdf counting

counting: $(CO).pdf
	./counter.sh

vlnka:
	vlna $(CO).tex
	vlna $(OBSAH).tex
	vlna $(REF).bib

$(CO).pdf: $(CO).ps
	dvipdf $(CO)

$(CO).ps: $(CO).dvi
	dvips $(CO)

$(CO).dvi: clean $(CO).tex $(REF).bib
	latex $(CO)
	bibtex $(CO)
	latex $(CO)
	latex $(CO)

$pdflatex: clean
	pdflatex $(CO)
	bibtex $(CO)
	pdflatex $(CO)
	pdflatex $(CO)

desky:
#	latex desky
#	dvips desky
#	dvipdf desky
	pdflatex desky

clean:
	rm -f *.dvi *.log $(CO).blg $(CO).bbl $(CO).toc *.aux $(CO).out $(CO).lof
	rm -f $(CO).pdf
	rm -f *~

pack:
	tar czvf bp-xjmeno.tar.gz *.tex *.bib *.bst ./fig/* ./cls/* Makefile Changelog
