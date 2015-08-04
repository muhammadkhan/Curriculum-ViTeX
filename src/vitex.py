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
    for child in texdoc.documentBody.contents:
        try:
            if child.name == "personal":
                print("personal option =",child.option)
                print("sizeof(option)=",len(child.option))
        except:
            print("errrrrrrrrrrrrr")
