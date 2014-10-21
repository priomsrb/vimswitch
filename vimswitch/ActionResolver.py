from .CommandLineParser import getCommandLineParser
from .InvalidArgsAction import createInvalidArgsAction
from .ShowCurrentProfileAction import createShowCurrentProfileAction
from .ShowVersionAction import createShowVersionAction
from .SwitchProfileAction import createSwitchProfileAction
from .UpdateProfileAction import createUpdateProfileAction


class ActionResolver:
    def __init__(self, app, commandLineParser):
        self.app = app
        self.commandLineParser = commandLineParser
        self.exitCode = 0

    def doActions(self):
        actionString = self.commandLineParser.action

        if actionString == 'switchProfile':
            action = createSwitchProfileAction(self.app)
            action.profile = self.commandLineParser.profile
        elif actionString == 'updateProfile':
            action = createUpdateProfileAction(self.app)
            action.profile = self.commandLineParser.profile
        elif actionString == 'showCurrentProfile':
            action = createShowCurrentProfileAction(self.app)
        elif actionString == 'showVersion':
            action = createShowVersionAction(self.app)
        else:
            action = createInvalidArgsAction(self.app)
            action.errorMessage = self.commandLineParser.errorMessage
            action.helpText = self.commandLineParser.helpText

        action.execute()
        self.exitCode = action.exitCode


def getActionResolver(app):
    return app.get('actionResolver', createActionResolver(app))


def createActionResolver(app):
    commandLineParser = getCommandLineParser(app)
    actionResolver = ActionResolver(app, commandLineParser)
    return actionResolver
