## Curriculum ViTeX
#  (C) 2015 Muhammad Khan
#
#  This software is licensed under
#  the MIT Public License

"""texdocument.py

This module defines the different objects that are
pertinent to LaTeX document.
"""

class LaTeXCommand:
    """
    Represents the object signified by a <command>
    in a *_structure.xml file
    """
    def __init__(self, name, contents, option=""):
        """
        Parameters: name - the name of the LaTeX command [string]
                    option - optional parameter for command [string] (optional)
                    contents - a list of the arguments
                               to the command [string list]

        Example: <command label='cmd' args='3'>
                   <option>opt</option>
                   <argument>arg1</argument>
                   <argument>arg2</argument>
                   <argument>arg3</argument>
                 </command>

                 will be represented as LaTeXCommand('cmd',[arg1,arg2,arg3], opt)
                 and corresponds to a line in LaTeX as follows:
                 \cmd[opt]{arg1}{arg2}{arg3}
        """
        self.name = name
        self.option = option
        self.contents = contents

class Environment:
    """The corresponding object signified by an <environment>
    tag in a *_structure.xml document.
    """
    def __init__(self, name, cmds_and_envs, option=""):
        """Creates blueprint for a LaTeX environment

        Parameters: name - the name of this environment [string]
                    cmds_and_envs - a list of the environment's contents
                                    including commands, other environments
                                    and pure text [list]
                    option - optional argument corresponding to this
                             environment's options [string] (optional)


        Example: <environment label='env'>
                    <option>opt</option>
                    .
                    .
                    .
                 </environment>
                 will translate to Environment(env, ..., opt)
                 and generate the following in LaTeX:
                    \begin{env}
                      .
                      .
                      .
                    \end{env}
        """
        self.name = name
        self.option = option
        self.cmds_and_envs = cmds_and_envs

class Body:
    """Represents the contents of the main part of the LaTeX
    document (everything between \begin{document}...\end{document}),
    and equivalently everything in between <document>...</document>
    in the *_structure.xml file.
    """
    def __init__(self, contents):
        """Creates a Body object and stores a list of the internal
        contents.

        Parameters: contents - a list of the commands, environments, and
                               pure text in the document [list]
        """
        self.contents = contents

class TeXStructure:
    """Object that represents an entire LaTeX document"""
    def __init__(self, fp):
        """Creates a new TexStructure object to be written
        at the given filepath.

        Parameters: fp - the filepath of this LaTeX document [string]
        """
        self.filepath = fp
        self.packages = []
        self.documentBody = None
