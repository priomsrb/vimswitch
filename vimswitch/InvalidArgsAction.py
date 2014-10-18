from .Action import Action


class InvalidArgsAction(Action):
    def __init__(self):
        Action.__init__(self)
        self.errorMessage = ''
        self.helpText = ''

    def execute(self):
        print(self.errorMessage)
        print(self.helpText)
        self.exitCode = -1


def createInvalidArgsAction(app):
    return InvalidArgsAction()
