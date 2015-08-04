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

def printResume(resm):
    print("PERSONAL:")
    print("Name:", resm.personal.name)
    print("Phone: (" + resm.personal.phone.areaCode + ")")
    print("Email:", resm.personal.email)
    print("Address:", resm.personal.address)
    print("Webiste:", resm.personal.website)
    print("EDUCATION:")
    for school in resm.education:
        print("School:", school.name)
        print("From:", school.beg, "To:", school.end)

def printTex(texdoc):
    print("FILE:", texdoc.filepath)
    for p in texdoc.packages:
        print("Package:", p[0])
        if len(p) > 1:
            print("    with option:", p[1])
    print("=====DOCUMENT========")
    for x in texdoc.documentBody.contents:
        print(x)

if __name__ == "__main__":
    parsed = rmlp(sys.argv[1]).res
    texdoc = xmlp(parsed, genXMLFilePath(sys.argv[2])).texdoc
    writeLaTeX(texdoc, sys.argv[2])
    print("Success!")
    #printTex(texdoc)
