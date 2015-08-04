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


def valid_num_argument_tags(commandNode):
    expected_value = int(commandNode.attrib["args"])
    ct = 0
    for child in commandNode:
        if child.tag == "argument":
            ct += 1
    return ct == expected_value

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
                texdoc.packages = self.loadPackages(child)
            elif(child.tag == "document"):
                texdoc.documentBody = self.loadBody(child)
            else:
                raise badxml("<" + child.tag + "> is not a valid direct child of <structure>")
        self.texdoc = texdoc

    def loadPackages(self, packagesNode):
        packages = []
        for packageNode in packagesNode:
            if packageNode.tag != "package":
                raise badxml("only <package> allowed")
            if len(packageNode) > 2:
                raise badxml("<package> can have at most 2 children")
            packageTuple = None
            try:
                if packageNode[0].tag == "option" and packageNode[1].tag == "value":
                    packageTuple = (packageNode[1].text, packageNode[0].text)
                elif packageNode[1].tag == "option" and packageNode[0].tag == "value":
                    packageTuple = (packageNode[0].text, packageNode[1].text)
                else:
                    raise badxml("<package> must have one of each <option> and <value>")
            except IndexError:
                packageTuple = (packageNode[0],)
            packages.append(packageTuple)
        return packages

    def loadBody(self, docNode):
        body = None
        cmds_and_envs = []
        if docNode.text is not None:
            cmds_and_envs.append(docNode.text)
        parse_routines = {
            "command" : self.parseCommand,
            "environment" : self.parseEnvironment,
            "iteration" : self.parseIteration,
            "property" : self.loadProperty
        }
        for child in docNode:
            #possibilities for child:
            #                       <command>
            #                       <environment>
            #                       <iteration>
            #                       <property />
            if child.tag in parse_routines.keys():
                r = parse_routines[child.tag]
                try:
                    cmds_and_envs.append(r(child))
                except TypeError:
                    cmds_and_envs.extend(r(child))
            else:
                raise badxml("<" + child.tag + "> is not a valid descendant of <document>")
                    
            # if child.tag == "command":
            #     cmds_and_envs.append(self.parseCommand(child))
            # elif child.tag == "environment":
            #     cmds_and_envs.append(self.parseEnvironment(child))
            # elif child.tag == "iteration":
            #     cmds_and_envs.extend(self.parseIteration(child))
            # elif child.tag == "property":
            #     cmds_and_envs.append(self.loadProperty(child))
            # else:
            #     raise badxml("<" + child.tag + "> is not a valid descendant of <document>")

            if child.tail is not None:
                cmds_and_envs.append(child.tail)

        body = Body(cmds_and_envs)
        return body

    def getIterCat(self, iterationNode):
        if iterationNode is None:
            return None
        try:
            return iterationNode.attrib["category"]
        except KeyError:
            raise badxml("<iteration> needs 'category'")

    def parseCommand(self, commandNode, iterationNode=None, iterationIndex = -1):
        #a <command> can only contain <argument>
        #or an <option>
        option = None
        try:
            if not valid_num_argument_tags(commandNode):
                raise badxml("number of <argument> tags not equal to value in 'args'")
            elif int(commandNode.attrib["args"]) < 0:
                raise badxml("cannot have negative 'args' value in <command>")
        except ValueError:
            raise badxml("<command> was not given a numerical value for 'args'")
        except KeyError:
            raise badxml("<command> was not supplied any 'args'")

        arguments = []
        for argument in commandNode:
            if argument.tag == "option":
                option = self.parseOption(argument, self.getIterCat(iterationNode))
                continue
            elif argument.tag != "argument":
                raise badxml("<command> can only contain <argument> tags")
            if len(argument) == 0: #aka pure text, no tags inside
                if argument.text is not None:
                    arguments.append(argument.text)
                # else:
                #     raise badxml("can't have empty <argument></argument>")
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
                        arguments.append(self.loadProperty(child, self.getIterCat(iterationNode), iterationIndex))
                    else:
                        raise badxml("<" + child.tag + "> is not a valid child for <argument>")

                    if child.tail is not None:
                        arguments.append(child.tail)
                        
        try:
            cmd = LaTeXCommand(commandNode.attrib["label"], arguments)
            if option is not None:
                cmd.option = option
            return cmd
        except KeyError:
            raise badxml("<command> is missing a label")

    def loadProperty(self, propertyNode, iterationSection=None, iterationIndex = -1):
        if len(propertyNode) > 0 or propertyNode.text is not None:
            raise badxml("poorly formatted <property> - cannot have children or encapsulate any text")
        resumeSection = ""
        resumeField = ""
        try:
            info = propertyNode.attrib
            resumeSection = info["category"]
            sectionField = info["content"]
        except KeyError:
            raise badxml("<property /> must have both 'category' and 'content'")
        #possibilities of parent:
        #                       the resume object itself
        #                       the education object, containing schools
        #                       the courses object, containing courses
        #                       the experiences obj, containing exp's
        parent = None
        categoryClassification = None
        if iterationSection is not None:
            parent = getattr(self.resumeObj, iterationSection)
            #parent would be a list
            #categoryClassification = getattr(parent[iterationIndex], resumeSection)
            categoryClassification = parent[iterationIndex]
        else:
            parent = self.resumeObj
            #parent would be an object
            categoryClassification = getattr(parent, resumeSection)
        try:
            return str(getattr(categoryClassification, sectionField))
        except AttributeError: return str(categoryClassification)

    def parseOption(self, optionNode, iterationSection=None):
        s = ""
        if optionNode.text is not None:
            s += optionNode.text
        #can only have <property> child
        for child in optionNode:
            if child.tag == "property":
                s += self.loadProperty(child, iterationSection)
                if child.tail is not None:
                    s += child.tail
            else:
                raise badxml("<option> can only have <property>")

    def parseIteration(self, iterationNode):
        section = None
        iterInfo = iterationNode.attrib
        try:
            section = getattr(self.resumeObj, iterInfo["category"])
        except KeyError:
            raise badxml("<iteration> missing a category")
        except AttributeError:
            raise badxml("\"" + iterInfo["category"] + "\" does not correspond to an appropriate iterable")
        iterContents = []
        for i in range(0, len(section)):
            if iterationNode.text is not None:
                iterContents.append(iterationNode.text)
            for child in iterationNode:
                #possibilities for child:
                #                       <command>
                #                       <property />
                if child.tag == "command":
                    iterContents.append(self.parseCommand(child, iterationNode, i))
                elif child.tag == "property":
                    iterContents.append(self.loadProperty(child, iterationNode, i))
                else:
                    raise badxml("<iteration> can only have <command> or <property /> children")
                    
                if child.tail is not None:
                    iterContents.append(child.tail)
        return iterContents

    def parseEnvironment(self, environmentNode):
        #presently, let's assume an environment
        # can never be iterated
        option = None
        cmds_and_envs = []
        if environmentNode.text is not None:
            cmds_and_envs.append(environmentNode.text)
        #possibilities for child:
        #                       <command>
        #                       <environment>
        #                       <iteration>
        #                       <option>
        for child in environmentNode:
            if child.tag == "command":
                cmds_and_envs.append(self.parseCommand(child))
            elif child.tag == "environment":
                cmds_and_envs.append(self.parseEnvironment(child))
            elif child.tag == "iteration":
                cmds_and_envs.extend(self.parseIteration(child))
            elif child.tag == "option":
                option = self.parseOption(child)
            else:
                raise badxml("<" + child.tag + "> cannot be in an environment")

            if child.tail is not None:
                cmds_and_envs.append(child.tail)

        try:
            env = Environment(environmentNode.attrib["label"], cmds_and_envs)
        except KeyError:
            raise badxml("<environment> missing a 'label' attribute")

        if option is not None:
            env.option = option
        return env
