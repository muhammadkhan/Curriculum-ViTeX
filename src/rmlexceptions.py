class InvalidRMLFileException(Exception):
    def __init__(self, message):
        super(InvalidRMLFileException, self).__init__(message)
