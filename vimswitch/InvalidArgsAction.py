class InvalidArgsAction():
    def __init__(self, errorMessage, helpText):
        self.errorMessage = errorMessage
        self.helpText = helpText

    def execute(self):
        print(self.errorMessage)
        print(self.helpText)
