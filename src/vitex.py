from os.path import pardir, sep
import sys
sys.path.append(pardir + sep)
from resumeParser import RMLParser as rmlp
from structureParser import StructureXMLParser as xmlp
from structureParser import SUFFIX

def genXMLFilePath(folder):
    path = "templates/"
    path += folder + "/"
    path += folder + SUFFIX
    return path

if __name__ == "__main__":
    parsed = rmlp(sys.argv[1])
    texdoc = xmlp(parsed, genXMLFilePath(sys.argv[2]))
    print("Success!")
