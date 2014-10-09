from .InvalidArgsAction import InvalidArgsAction
from .ShowCurrentProfileAction import createShowCurrentProfileAction
from .SwitchProfileAction import createSwitchProfileAction
from .CommandLineParser import getCommandLineParser


class ActionResolver:
    def __init__(self, app, commandLineParser):
        self.app = app
        self.commandLineParser = commandLineParser
        self.exitCode = 0

    def doActions(self):
        action = self.commandLineParser.action
        if action == 'switchProfile':
            switchProfileAction = createSwitchProfileAction(self.app)
            switchProfileAction.switchToProfile(self.commandLineParser.profile)
        elif action == 'showCurrentProfile':
            showCurrentProfileAction = createShowCurrentProfileAction(self.app)
            showCurrentProfileAction.execute()
        else:
            errorMessage = self.commandLineParser.errorMessage
            helpText = self.commandLineParser.helpText
            invalidArgsAction = InvalidArgsAction(errorMessage, helpText)
            invalidArgsAction.execute()
            self.exitCode = -1


def getActionResolver(app):
    return app.get('actionResolver', createActionResolver(app))


def createActionResolver(app):
    commandLineParser = getCommandLineParser(app)
    actionResolver = ActionResolver(app, commandLineParser)
    return actionResolver
