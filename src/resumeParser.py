import xml.etree.ElementTree as ET
from rmlexceptions import InvalidRMLFileException

class RMLParser:
    def __init__(self, rmlFilePath):
        resumeTree = ET.parse(rmlFilePath)
        resumeRoot = resumeTree.getroot()
        if(resumeRoot.tag != "resume"):
            raise InvalidRMLFileException("Root tag of RML file is not <resume>")
        
