#!/usr/bin/bash

# author: Muhammad Khan (mhk98@cornell.edu)
# usage: "cvitex.sh <rml_file_name>
#                     <template_1_dir> [<template_2_dir> ...]"

# $1 refers to RML file
# $2, $3,...  refer to names of directories inside templates/

if [ $# -lt 1 ]; then
    echo ERROR: Insufficient number of arguments
else
    python vitex.py $@
fi
