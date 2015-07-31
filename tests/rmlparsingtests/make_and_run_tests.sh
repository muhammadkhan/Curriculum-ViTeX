#!/usr/bin/bash

#author: Muhammad Khan (mhk98@cornel.edu)
#usage: "make_and_run_tests.sh"
#        will take <x.rml> and create <text_x.py>
#        will then run each .py file

#idk if it's poor style to write entire files using shell

import_parser="from src.resumeParser import RMLParser as rmlp"
import_exc="from src.cvitexexceptions import InvalidRMLFileException as badrml"
import_sys="import sys"
import_os="from os.path import pardir, sep"

log_file="RESULTS.log"
touch $log_file

if [ $# -ge 1 ]; then
    echo ERROR: Too many arguments
else
    for rmlFile in *.rml; do
	fname=$(echo $rmlFile | cut -d '.' -f 1)
	file=test_$fname.py
	touch $file
	echo $import_sys >> $file
	echo $import_os >> $file
	echo "sys.path.append(pardir + sep + pardir + sep)" >> $file
	echo $import_parser >> $file
	echo $import_exc >> $file
	echo "if __name__ == \"__main__\":" >> $file
	echo "  try:" >> $file
	echo "    parsed = rmlp(\"${rmlFile}\")" >> $file
	echo "    print(\"test success!\")" >> $file
	echo "  except badrml:" >> $file
	echo "    e = sys.exc_info()[0]" >> $file
	echo "    print(\"exception caught: \" + str(e))" >> $file

	#log printing
	echo "#############################" >> $log_file
	echo "TEST: ${file}" >> $log_file
	echo "#############################" >> $log_file
	python $file >> $log_file
	echo >> $log_file
	echo >> $log_file
    done
fi
