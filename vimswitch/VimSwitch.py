from .ActionResolver import getActionResolver
from .Application import Application
from .ApplicationDirs import getApplicationDirs
from .CommandLineParser import getCommandLineParser
from .ConfigFile import getConfigFile
from .Settings import getSettings


class VimSwitch:
    def __init__(self, app=Application()):
        self.app = app
        self.raiseExceptions = False

    def main(self, argv):
        """
        Runs VimSwitch with the given args. Returns 0 on success, or -1 if an
        error occurred.
        """
        try:
            self.loadSettings()
            commandLineParser = getCommandLineParser(self.app)
            commandLineParser.parse(argv)
            actionResolver = getActionResolver(self.app)
            actionResolver.doActions()
            self.saveSettings()
            return actionResolver.exitCode
        except Exception as e:
            message = 'Error: %s' % str(e)
            print(message)
            return -1

    def loadSettings(self):
        applicationDirs = getApplicationDirs(self.app)
        applicationDirs.createIfNone()
        settings = getSettings(self.app)
        configFile = getConfigFile(self.app)
        configFile.loadSettings(settings, settings.configFilePath)

    def saveSettings(self):
        settings = getSettings(self.app)
        configFile = getConfigFile(self.app)
        configFile.saveSettings(settings, settings.configFilePath)
