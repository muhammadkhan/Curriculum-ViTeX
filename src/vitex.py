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

if __name__ == "__main__":
    resm = rmlp(sys.argv[1]).res
    texdoc = xmlp(resm, genXMLFilePath(sys.argv[2])).texdoc
    writeLaTeX(texdoc, sys.argv[2])
    print("EXPERIENCES: length=", len(resm.experiences))
    for exp in resm.experiences:
        print(exp.title,"@",exp.employer,"from",exp.duration)
