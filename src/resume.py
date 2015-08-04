class Personal:
    def __init__(self,name="",phone=None,email="",address="",web=""):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.website = web

class PhoneNumber:
    #Precondition: len(num) == 10
    #              first 3 chars of num correspond to area code
    def __init__(self, num, ext = ""):
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
    def __init__(self, b="", e=""):
        self.beginning = b
        self.end = e
        self.name = ""
        self.majors = []
        self.degrees = []
        self.gpa = None
        self.comment = ""

class Experience:
    def __init__(self):
        self.title = ""
        self.employer = ""
        self.duration = ""
        self.description = ""
        
class Resume:
    def __init__(self):
        self.personal = None
        self.education = []
        self.courses = []
        self.experiences = []
