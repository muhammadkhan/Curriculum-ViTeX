class LaTeXCommand:
    """
    Represents the object represented by a <command>
    in a *_structure.xml file
    """
    def __init__(self, name, contents):
        """
        Parameters: name - the name of the LaTeX command
                    contents - a list of the arguments
                               to the command

        Example: <command label='cmd' args='3'>
                   <argument>arg1</argument>
                   <argument>arg2</argument>
                   <argument>arg3</argument>
                 </command>

                 will be represented as LaTeXCommand('cmd', [arg1,arg2,arg3])
                 and corresponds to a line in LaTeX as follows:
                 \cmd{arg1}{arg2}{arg3}
        """
        self.name = name
        self.contents = contents

class Body:
    

class TeXStructure:
    def __init__(self, fp):
        self.filepath = fp
        self.packages = []
        self.documentBody = None
