#!/bin/sh

pdftotext projekt.pdf
chars=$((`cat projekt.txt | wc -m`))
echo "Bezny rozsah: 30-40 normostran."
echo "Aktualni pocet normostran v projektu:" $(($chars / 1800 ))
echo "Procentualne hotovo:" $(($chars / 1800 * 100 / 30 )) "%"
rm projekt.txt
