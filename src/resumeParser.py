import xml.etree.ElementTree as ET
from resume import *
from cvitexexceptions import InvalidRMLFileException as badrml

class RMLParser:
    def __init__(self, rmlFilePath):
        resumeTree = ET.parse(rmlFilePath)
        resumeRoot = resumeTree.getroot()
        if(resumeRoot.tag != "resume"):
            raise badrml("Root tag of RML file is not <resume>")
        resm = Resume()
        for child in resumeRoot:
            # possibilities for child:
            #                        <personal>
            #                        <education>
            #                        <courses>
            #                        <experiences>
            if(child.tag == "personal"):
                resm.personal = self.loadPersonal(child)
            elif(child.tag == "education"):
                resm.education = self.loadEducation(child)
            elif(child.tag == "courses"):
                resm.courses = self.loadCourses(child)
            elif(child.tag == "experiences"):
                resm.experiences = self.loadExperiences(child)
            else:
                raise badrml("<" + child.tag + "> is not a valid descendant of <resume>")

        self.res = resm

    def loadExperiences(self, experiencesNode):
        experiences = []

        for experNode in experiencesNode:
            if(experNode.tag != "experience"):
                raise badrml("only <experience> allowed")
            experience = Experience()
            fields = {
                "title" : experience.title,
                "employer" : experience.employer,
                "duration" : experience.duration,
                "description" : experience.desc
            }
            for child in experNode:
                #possibilities for child:
                #                       <title>
                #                       <employer>
                #                       <duration>
                #                       <description>
                if(child.tag in fields.keys()):
                    fields[child.tag] = child.text
        
        return experiences

    def loadCourses(self, coursesNode):
        courses = []
        for i in range(0,len(coursesNode)):
            course = coursesNode[i]
            if(course.tag != "course"):
                raise badrml("only <course> allowed")
            courses.append(course.text)
        return courses

    def loadEducation(self, educationNode):
        education = []
        for schoolNode in educationNode:
            if(schoolNode.tag != "school"):
                raise badrml("<school> is the only valid child for <education>")
            schoolDict = schoolNode.attrib
            school = School(schoolDict["beginning"], schoolDict["end"])
            for child in schoolNode:
                #possibilites for child:
                #                      <name>
                #                      <majors>
                #                      <degrees>
                #                      <gpa>
                #                      <comment>
                if(child.tag == "name"):
                    school.name = child.text
                elif(child.tag == "majors"):
                    majors = []
                    for i in range(0,len(child)):
                        if(child[i].tag != "major"):
                            raise badrml("only <major> allowed")
                        majors.append(child[i].text)
                    school.majors = majors
                elif(child.tag == "degrees"):
                    degrees = []
                    for i in range(0,len(child)):
                        if(child[i].tag != "degree"):
                            raise badrml("only <degree> allowed")
                        degrees.append(child[i].text)
                    school.degrees = degrees
                elif(child.tag == "gpa"):
                    gpaInfo = child.attrib
                    school.gpaActual = float(gpaInfo["value"])
                    school.gpaMax = float(gpaInfo["maximum"])
                elif(child.tag == "comment"):
                    school.comment = child.text
            education.append(school)
        return education

    def loadPersonal(self, personalNode):
        personal = Personal()
        for child in personalNode:
            #possibilities for child:
            #                       <name>
            #                       <phone>
            #                       <email>
            #                       <address>
            #                       <website>
            if(child.tag == "name"):
                personal.name = child.text
            elif(child.tag == "phone"):
                ext = ""
                #phone number validation
                extSplit = child.text.lower().split("x")
                if(len(extSplit) > 2):
                    raise badrml("phone numbers must have at most 1 extension")
                elif(len(extSplit) == 2):
                    ext = extSplit[1]

                phone_raw = extSplit[0]
                if(len(phone_raw) != 10):
                    raise badrml("phone numbers (excluding extension) must have a length of 10")
                personal.phone = PhoneNumber(phone_raw, ext)
            elif(child.tag == "email"):
                personal.email = child.text
            elif(child.tag == "address"):
                personal.address = child.text
            elif(child.tag == "website"):
                personal.website = child.text
            else:
                raise badrml("<" + child.tag + "> is not a valid child for <personal>")
        return personal
