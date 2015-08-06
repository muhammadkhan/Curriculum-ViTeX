## Curriculum ViTeX
#  (C) 2015 Muhammad Khan
#
#  This software is licensed under
#  the MIT Public License

"""resumeParser.py

This module defines a parser object which is
used to parse an RML document and generate a
full Resume object.
"""

import xml.etree.ElementTree as ET
from resume import *
from cvitexexceptions import InvalidRMLFileException as badrml

class RMLParser:
    """Object that represents a parser for an RML file"""
    def __init__(self, rmlFilePath):
        """Creates a new parser object with a 'resm' property
        of type Resume (defined in resume.py)

        Parameters: rmlFilePath - the path pointing to the RML
                                  file of interest [string]
        """
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
            #                        <skills>
            if(child.tag == "personal"):
                resm.personal = self.loadPersonal(child)
            elif(child.tag == "education"):
                resm.education = self.loadEducation(child)
            elif(child.tag == "courses"):
                resm.courses = self.loadCourses(child)
            elif(child.tag == "experiences"):
                resm.experiences = self.loadExperiences(child)
            elif(child.tag == "skills"):
                resm.skills = self.loadSkills(child)
            else:
                raise badrml("<" + child.tag + "> is not a valid descendant of <resume>")

        self.res = resm

    def loadSkills(self, skillsNode):
        """Takes a <skills> tag and returns a list of Skill objects

        Parameters: skillsNode - the object corresponding to the
                                 <skills> tag [ElementTree tag]

        Returns: a list of the different Skill objects that skillsNode
                 encapsulates
        """
        skills = []
        for skillNode in skillsNode:
            if skillNode.tag != "skill":
                raise badrml("only <skill> allowed in <skills>")
            if len(skillNode) > 0:
                raise badrml("<skill> cannot have any children")
            if skillNode.text is None or len(skillNode.text.strip()) == 0:
                raise badrml("empty <skill> somewhere")
            try:
                lvl = skillNode.attrib["level"]
                skills.append(Skill(skillNode.text, lvl))
            except KeyError:
                raise badrml("<skill> missing 'level' attribute")
            except ValueError:
                raise badrml("'" + lvl + "' is an invalid skill level")
        return skills
                

    def loadExperiences(self, experiencesNode):
        """Takes an <experiences> tag and returns a list of Experience objects

        Parameters: experiencesNode - the object corresponding to the
                                 <experiences> tag [ElementTree tag]

        Returns: a list of the different Experience objects that experiencesNode encapsulates
        """
        experiences = []

        for experNode in experiencesNode:
            if(experNode.tag != "experience"):
                raise badrml("only <experience> allowed")
            experience = Experience()
            fields = ["title","employer","duration","description"]
            for child in experNode:
                #possibilities for child:
                #                       <title>
                #                       <employer>
                #                       <duration>
                #                       <description>
                if child.tag in fields:
                    #fields[child.tag] = child.text
                    setattr(experience, child.tag, child.text)
                else:
                    raise badrml("<experience> can only take so much")
            experiences.append(experience)
                    
        return experiences

    def loadCourses(self, coursesNode):
        """Takes a <courses> tag and returns a list of the courses

        Parameters: coursesNode - the object corresponding to the
                                 <courses> tag [ElementTree tag]

        Returns: a list of the different courses (strings) that coursesNode
                 encapsulates
        """
        courses = []
        for i in range(0,len(coursesNode)):
            course = coursesNode[i]
            if(course.tag != "course"):
                raise badrml("only <course> allowed")
            courses.append(course.text)
        return courses

    def loadEducation(self, educationNode):
        """Takes an <education> tag and returns a list of School objects

        Parameters: educationNode - the object corresponding to the
                                 <education> tag [ElementTree tag]

        Returns: a list of the different School objects that educationNode
                 encapsulates
        """
        education = []
        for schoolNode in educationNode:
            if(schoolNode.tag != "school"):
                raise badrml("<school> is the only valid child for <education>")
            schoolDict = schoolNode.attrib
            schoolBeg = ""
            schoolEnd = ""
            try:
                schoolBeg = schoolDict["beginning"]
                schoolEnd = schoolDict["end"]
            except KeyError:
                raise badrml("<school> missing 'beginning' and 'end' attributes")
            name = ""
            majors = []
            degrees = []
            gpa = None
            comment = ""
            for child in schoolNode:
                #possibilites for child:
                #                      <name>
                #                      <majors>
                #                      <degrees>
                #                      <gpa>
                #                      <comment>
                if(child.tag == "name"):
                    name = child.text
                elif(child.tag == "majors"):
                    for i in range(0,len(child)):
                        if(child[i].tag != "major"):
                            raise badrml("only <major> allowed")
                        majors.append(child[i].text)
                elif(child.tag == "degrees"):
                    for i in range(0,len(child)):
                        if(child[i].tag != "degree"):
                            raise badrml("only <degree> allowed")
                        degrees.append(child[i].text)
                elif(child.tag == "gpa"):
                    gpaInfo = child.attrib
                    try:
                        gpaActual = float(gpaInfo["value"])
                        gpaMax = float(gpaInfo["maximum"])
                        gpa = (gpaActual, gpaMax)
                    except KeyError:
                        raise badrml("missing gpa attributes")
                elif(child.tag == "comment"):
                    comment = child.text
                else:
                    raise badrml("some invalid school children")
            school = School(schoolBeg, schoolEnd, name, majors, degrees, gpa, comment)
            education.append(school)
        return education

    def loadPersonal(self, personalNode):
        """Converts a <personal> tag into a Personal object

        Parameters: personalNode - the object corresponding to the
                                 <personal> tag [ElementTree tag]

        Returns: The Personal object with the appropriate information
                 filled in
        """
        name = ""
        phone = None
        email = ""
        address = ""
        web = ""
        for child in personalNode:
            #possibilities for child:
            #                       <name>
            #                       <phone>
            #                       <email>
            #                       <address>
            #                       <website>
            if(child.tag == "name"):
                name = child.text
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
                phone = PhoneNumber(phone_raw, ext)
            elif(child.tag == "email"):
                email = child.text
            elif(child.tag == "address"):
                address = child.text
            elif(child.tag == "website"):
                website = child.text
            else:
                raise badrml("<" + child.tag + "> is not a valid child for <personal>")
        return Personal(name, phone, email, address, web)
