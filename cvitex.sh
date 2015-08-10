#!/usr/bin/bash

# author: Muhammad Khan (mhk98@cornell.edu)
# usage: "cvitex.sh <rml_file_name>
#                     <template_1_dir> [<template_2_dir> ...]"
#        optional: add flag -p or --pdf to generate the pdf automatically
#                  from the tex file created

arg1="$1"
pdf_choice=0
LATEX_CMD="pdflatex"
BASE_DIR=$(pwd)
case $arg1 in
    -p | --pdf)
	pdf_choice=1
	shift
	;;
    *)
	;;
esac
	
# after the shift:
# $1 refers to RML file
# $2, $3,...  refer to names of directories inside templates/

if [ $# -lt 1 ]; then
    echo ERROR: Insufficient number of arguments
else
    python src/vitex.py $@

    if [ $pdf_choice -gt 0 ]; then
	#check if pdflatex is installed or not
	if ! type "$LATEX_CMD" > /dev/null; then
	    #pdflatex is not installed
	    echo "Sorry, you don't have pdflatex"
	else
	    #pdflatex is installed
	    shift #shift past the RML file name, so now
	          #$@ includes only the templates
	    while [ $# -gt 0 ]; do
		cd $BASE_DIR #switch back
		d=templates/$1
		cd $d
		$LATEX_CMD $1_cv.tex
		shift
	    done
	fi
    fi
fi
