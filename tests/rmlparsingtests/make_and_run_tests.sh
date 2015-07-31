#!/usr/bin/bash

#author: Muhammad Khan (mhk98@cornel.edu)
#usage: "make_and_run_tests.sh"
#        will take <x.rml> and create <text_x.py>
#        will then run each .py file

if [ $# -ge 1 ]; then
    echo ERROR: Too many arguments
else
    for rmlFile in *.rml; do
	fname=$(echo $rmlFile | cut -d '.' -f 1)
	touch test_$fname.py
    done
fi
