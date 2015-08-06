## Curriculum ViTeX
#  (C) 2015 Muhammad Khan
#
#  This software is licensed under
#  the MIT Public License

"""latex_writer.py

This module defines the different functions used
to take a TeXStructure object and use it to actually
write a valid LaTeX file.
"""

from resume import *
from texdocument import *
import os.path

DEFAULT_CLASS = "article"

def documentClass(cls):
    f = "templates/" + cls + "/" + cls + ".cls"
    if os.path.isfile(f):
        return cls
    return DEFAULT_CLASS

def packageStr(packageTuple):
    base = "\\usepackage"
    opt = ""
    if len(packageTuple) == 2:
        opt = "[" + packageTuple[1] + "]"
    p = "{" + packageTuple[0] + "}"
    return (base + opt + p)

def commandStr(cmd):
    c = "\\" + cmd.name
    if len(cmd.option) > 0:
        c += "[" + cmd.option + "]"

    for x in cmd.contents:
        c += "{" + x + "}"
    return c

def environmentWrite(fileObj, env):
    fileObj.write("\\begin")
    if len(env.option) > 0:
        fileObj.write("[" + env.option + "]")
    fileObj.write("{" + env.name + "}")

    for obj in env.cmds_and_envs:
        if type(obj) is LaTeXCommand:
            fileObj.write(commandStr(obj) + "\n")
        elif type(obj) is str:
            fileObj.write(obj + "\n")
        elif type(obj) is Environment:
            environmentWrite(fileObj, obj)
    
    fileObj.write("\\end{" + env.name + "}\n")

def writeLaTeX(texdoc, cls):
    # in structureParser.py, texdoc's 'filepath'
    # attribute is already a full path
    with open(texdoc.filepath, "w") as texfile:
        #write the preamble
        texfile.write("\\documentclass{" + documentClass(cls) + "}\n")
        for pTup in texdoc.packages:
            texfile.write(packageStr(pTup) + "\n")
        #start writing the body
        texfile.write("\\begin{document}\n")

        for content in texdoc.documentBody.contents:
            if type(content) is LaTeXCommand:
                texfile.write(commandStr(content) + "\n")
            elif type(content) is str:
                texfile.write(content + "\n")
            elif type(content) is Environment:
                environmentWrite(texfile, content)
        
        texfile.write("\\end{document}")
