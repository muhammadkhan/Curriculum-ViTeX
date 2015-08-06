## Curriculum ViTeX
#  (C) 2015 Muhammad Khan
#
#  This software is licensed under
#  the MIT Public License

"""resume.py

This module defines the objects (more like structs)
that comprise a resume. They correspond logically
to sections in an RML file.
"""

class Personal:
    """Object that represents the 'personal' section of an RML file"""
    def __init__(self, name, phone, email, address, web):
        """Creates a new Personal object

        Parameters: name - the name to whom the resume belongs [string]
                    phone - the resume-holder's phone number
                    email - -------,,---------- email address
                    address - -----,,---------- mailing address
                    web -     -----,,---------- personal website
        """
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.website = web

class PhoneNumber:
    """Object that represents the phone number
    in an RML file. The __str__() will render
    the phone number 1234567890 in the following format:

    (123)456-7890
    """
    def __init__(self, num, ext = ""):
        """Creates a new PhoneNumber object, taking in the phone
        number as a string of 10 digits, with an optional extension
        following the digits, separated by an 'x' character

        Parameters: num - the phone number [numerical string]
                    ext - the extension (optional) [numerical string]

        Preconditions: len(num) == 10
                       The first 3 digits of num should correspond
                       to the area code
        """
        self.ext = ext
        self.areaCode = num[0:3]
        self.middleThree = num[3:6]
        self.lastFour = num[6:]

    def __str__(self):
        s = "(" + self.areaCode + ")"
        s += self.middleThree + "-"
        s += self.lastFour
        if len(self.ext) > 0:
            s += "x" + self.ext
        return s

class School:
    """Object that represents a school in an RML document"""
    def __init__(self, b, e, name, majors, degrees, gpa, comment = ""):
        """Creates a new School object

        Parameters: b - the time the user began this school [numerical string]
                    e - the time the user ended this school [numerical string]
                    name - the name of this school [string]
                    majors - a list of the majors fulfilled while at this school [string list]
                    degrees - a list of the degrees achieved at this school [string list]
                    gpa - a 2-tuple (v,m) where v represents the GPA obtained and m represents the maximum possible GPA (float,float tuple)
                    comment - any description of the user's time at this chool [string] (optional)
        """
        self.beginning = b
        self.end = e
        self.name = name
        self.majors = majors
        self.degrees = degrees
        self.gpa = gpa
        self.comment = comment

class Experience:
    """Object that represents an experience in an RML document"""
    def __init__(self):
        self.title = ""
        self.employer = ""
        self.duration = ""
        self.description = ""

class Skill:
    """Object that represents a skill in an RML document"""
    def __init__(self, name, level):
        """Creates a new Skill object

        Parameters: name - the name of this particular skill [string]
                    level - the level associated with this particular skill [string]
                            Performs a check to make sure level is one of
                            the allowed values
        """
        LEVELS = ["expert", "good", "average", "basic"]
        if level not in LEVELS:
            raise ValueError("invalid 'level' - could not instantiate skill")
        self.level = level
        self.name = name

    def __str__(self):
        return self.name + " (" + self.level + ")"
        
class Resume:
    """Object that represents an entire resume RML document"""
    def __init__(self):
        self.personal = None
        self.education = []
        self.courses = []
        self.experiences = []
        self.skills = []
