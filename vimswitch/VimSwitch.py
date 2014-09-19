from ActionResolver import getActionResolver
from Application import Application
from CommandLineParser import getCommandLineParser
from ApplicationDirs import getApplicationDirs


class VimSwitch:
    def __init__(self, app=Application()):
        self.app = app
        self.raiseExceptions = False

    def run(self, argv):
        """
        Runs VimSwitch with the given args. Returns 0 on success, or -1 if an
        error occurred.
        """
        try:
            applicationDirs = getApplicationDirs(self.app)
            applicationDirs.createIfNone()

            commandLineParser = getCommandLineParser(self.app)
            commandLineParser.parse(argv)
            actionResolver = getActionResolver(self.app)
            actionResolver.doActions()
            return actionResolver.exitCode
        except Exception as e:
            message = 'Error: %s' % e.message
            print(message)
            return -1
