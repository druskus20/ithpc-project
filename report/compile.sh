#!/bin/sh

panc="pandoc --listings -H listings-setup.tex"

for i in *.md; do
    echo "Compiling $i to $(basename -s .md $i).pdf"
    rm "$(basename -s .md $i).pdf"
    $panc -o "$(basename -s .md $i).pdf" $i
done

