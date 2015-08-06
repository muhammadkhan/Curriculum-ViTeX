## Curriculum ViTeX
#  (C) 2015 Muhammad Khan
#
#  This software is licensed under
#  the MIT Public License

"""vitex.py

This module defines the main module to be run
by cvitex.sh.
"""

from os.path import pardir, sep
import sys
sys.path.append(pardir + sep)
from resumeParser import RMLParser as rmlp
from structureParser import StructureXMLParser as xmlp
from structureParser import SUFFIX
from latex_writer import writeLaTeX

def genXMLFilePath(folder):
    path = "templates/"
    path += folder + "/"
    path += folder + SUFFIX
    return path

def main(rmlFilePath, templatesList):
    """This is the function that can be used
    if vitex.py is imported as a library module instead
    of being run as main
    """
    resm = rmlp(rmlFilePath).res
    for template in templatesList:
        texdoc = xmlp(resm, genXMLFilePath(template)).texdoc
        writeLaTeX(texdoc, template)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
