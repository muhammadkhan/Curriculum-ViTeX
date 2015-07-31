#!/usr/bin/bash

#author: Muhammad Khan (mhk98@cornel.edu)
#usage: "make_and_run_tests.sh"
#        will take <x.rml> and create <text_x.py>
#        will then run each .py file

import1="from src.resumeParser import RMLParser as rmlp"
import2="from src.cvitexexceptions import InvalidRMLException as badrml"
import3="import sys"

if [ $# -ge 1 ]; then
    echo ERROR: Too many arguments
else
    for rmlFile in *.rml; do
	fname=$(echo $rmlFile | cut -d '.' -f 1)
	file=test_$fname.py
	touch $file
	echo $import1 >> $file
	echo $import2 >> $file
	echo $import3 >> $file
	echo "if __name__ == \"__main__\":" >> $file
	echo "  try:" >> $file
	echo "    parsed = rmlp(${rmlFile})" >> $file
	echo "    print(\"test success!\")" >> $file
	echo "  except badrml:" >> $file
	echo "    e = sys.exc_info()[0]" >> $file
	echo "    print(\"exception caught: \" + str(e))" >> $file
    done
fi
