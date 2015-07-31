import xml.etree.ElementTree as ET
from resume import *
from cvitexexceptions import InvalidStructureXMLFileException as badxml
from texdocument import *

SUFFIX = "_structure.xml"

def genTexFilePath(sxmlFilePath):
    """Assuming that the XML file name
       is of the format <*>_structure.xml, will generate the
       corresponding tex file: <*>_cv.tex
    """
    suffix = sxmlFilePath[-len(SUFFIX):]
    if(suffix != SUFFIX):
        raise badxml("Invalid name for XML file")
    prefix = sxmlFilePath[:-len(SUFFIX)]
    return prefix + "_cv.tex"

class StructureXMLParser:
    def __init__(self, resumeObj, sxmlFilePath):
        xmlTree = ET.parse(sxmlFilePath)
        structureTag = xmlTree.getroot()
        texdoc = TeXStructure(genTexFilePath(sxmlFilePath))
        if(structureTag.tag != "structure"):
            raise badxml("Root of XML file is not <structure>")
        for child in structureTag:
            #possibilities for child:
            #                      <packages>
            #                      <document>
            if(child.tag == "packages"):
                texdoc.packages = loadPackages(child, resumeObj)
            elif(child.tag == "document"):
                texdoc.documentBody = loadBody(child, resumeObj)
            else:
                raise badxml("<" + child.tag + "> is not a valid direct child of <structure>")

        return texdoc

    def loadPackages(self, packagesNode, resumeObj):
        packages = []
        for packageNode in packagesNode:
            if packageNode.tag != "package":
                raise badxml("only <package> allowed")
            if len(packageNode != 2):
                raise badxml("<package> can only have 2 children")
            packageTuple = None
            if packageNode[0] == "option" and packageNode[1] == "value":
                packageTuple = (packageNode[0].text, packageNode[1].text)
            else:
                packageTuple = (packageNode[1].text, packageNode[0].text)
            packages.append(packageTuple)
        return packages

    def loadBody(self, documentNode, resumeObj):
        pass
