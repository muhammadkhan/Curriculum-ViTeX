import xml.etree.ElementTree as ET
from resume import *
from cvitexexceptions import InvalidStructureXMLFileException as badxml
from texdocument import *

SUFFIX = "_structure.xml"

def getEntireText(node):
    """
    Used to get the entire text for element [node]
    Example: if t refers to '<tag>1234<tag2>56</tag2>7890</tag>'
             then getEntireText(t) = '1234<tag2>56</tag2>7890'
    """
    return "".join([node.text] + [ET.tostring(child) for child in node.getchildren()])

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
        self.resumeObj = resumeObj
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
                texdoc.packages = loadPackages(child)
            elif(child.tag == "document"):
                texdoc.documentBody = loadBody(child)
            else:
                raise badxml("<" + child.tag + "> is not a valid direct child of <structure>")

        return texdoc

    def loadPackages(self, packagesNode):
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

    def loadBody(self, documentNode):
        body = None
        commands = []
        for child in documentNode:
            #possibilities for child:
            #                       <command>
            #                       <environment>
            #                       <iteration>
            #                       <text>
            if child.tag == "command":
                commands.append(self.parseCommand(child))
            elif child.tag == "environment":
                pass
            elif child.tag == "iteration":
                pass
            elif child.tag == "text":
                pass
            else:
                raise badxml("<" + child.tag + "> not a valid descendant of <document>")
        return body

    def parseCommand(self, commandNode):
        #a <command> can only contain <argument>
        commandNodeInfo = commandNode.attrib
        try:
            if len(commandNode) != int(commandNodeInfo["args"]):
                raise badxml("number of <argument> tags not equal to value in 'args'")
            elif int(commandNodeInfo["args"]) < 0:
                raise badxml("cannot have negative 'args' value in <command>")
        except ValueError:
            raise badxml("<command> was not given a numerical value for 'args'")
        except KeyError:
            raise badxml("<command> was not supplied any 'args'")

        arguments = []
        for argument in commandNode:
            if argument.tag != "argument":
                raise badxml("<command> can only contain <argument> tags")
            if len(argument) == 0: #aka pure text, no tags inside
                if argument.text is not None:
                    arguments.append(argument.text)
                else:
                    raise badxml("can't have empty <argument></argument>")
            else:
                #WATCH OUT FOR: there may be text and children tags coupled randomly
                #    like - <argument>
                #              text text <command ...>...</command> more text <property... /> text
                #           </argument>
                if argument.text is not None:
                    arguments.append(argument.text)
                for child in argument:
                    #possibilities for child:
                    #                       <command>
                    #                       <property>
                    if child.tag == "command":
                        #recursion ftw
                        arguments.extend(self.parseCommand(child))
                    elif child.tag == "property":
                        pass
                    else:
                        raise badxml("<" + child.tag + "> is not a valid child for <argument>")

                    if child.tail is not None:
                        arguments.append(child.tail)
                        
        try:
            return LaTeXCommand(commandNodeInfo["label"], arguments)
        except KeyError:
            raise badxml("<command> is missing a label")

    def loadProperty(self, propertyNode):
        if len(propertyNode) > 0 or propertyNode.text is not None or propertyNode.tail is not None:
            raise badxml("poorly formatted <property> - cannot have children or encapsulate any text")
        resumeSection = ""
        resumeField = ""
        try:
            info = propertyNode.attrib
            resumeSection = info["category"]
            sectionField = info["content"]
        except KeyError:
            raise badxml("<property /> must have both 'category' and 'content'")
        #Possibilities for resumeSection:
        #                               "personal"
        #                               "education"
        #                               "courses"
        #                               "experiences"
        try:
            section = getattr(self.resumeObj, resumeSection)
            
