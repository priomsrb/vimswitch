from InvalidArgsAction import InvalidArgsAction
from ShortHelpAction import ShortHelpAction
from SwitchProfileAction import createSwitchProfileAction
from CommandLineParser import getCommandLineParser


class ActionResolver:
    def __init__(self, app, commandLineParser):
        self.app = app
        self.commandLineParser = commandLineParser

    def doActions(self):
        action = self.commandLineParser.action
        if action == 'switchProfile':
            switchProfileAction = createSwitchProfileAction(self.app)
            switchProfileAction.switchToProfile(self.commandLineParser.profile)
        elif action == 'shortHelp':
            ShortHelpAction().execute()
        else:
            InvalidArgsAction().execute()


def getActionResolver(app):
    return app.get('actionResolver', createActionResolver(app))


def createActionResolver(app):
    commandLineParser = getCommandLineParser(app)
    actionResolver = ActionResolver(app, commandLineParser)
    return actionResolver
