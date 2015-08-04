class LaTeXCommand:
    """
    Represents the object represented by a <command>
    in a *_structure.xml file
    """
    def __init__(self, name, option="", contents):
        """
        Parameters: name - the name of the LaTeX command
                    option - optional parameter for command
                    contents - a list of the arguments
                               to the command

        Example: <command label='cmd' args='3'>
                   <option>opt</option>
                   <argument>arg1</argument>
                   <argument>arg2</argument>
                   <argument>arg3</argument>
                 </command>

                 will be represented as LaTeXCommand('cmd', opt,[arg1,arg2,arg3])
                 and corresponds to a line in LaTeX as follows:
                 \cmd[opt]{arg1}{arg2}{arg3}
        """
        self.name = name
        self.option = option
        self.contents = contents

class Environment:
    def __init__(self, name, option = "", cmds_and_envs):
        self.name = name
        self.option = option
        self.cmds_and_envs = cmds_and_envs

class Body:
    def __init__(self, contents):
        self.contents = contents

class TeXStructure:
    def __init__(self, fp):
        self.filepath = fp
        self.packages = []
        self.documentBody = None
