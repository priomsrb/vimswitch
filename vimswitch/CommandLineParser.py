from .Profile import Profile


class CommandLineParser:
    def parse(self, argv):
        if len(argv) == 1:
            self.action = 'shortHelp'
        elif len(argv) == 2:
            self.action = 'switchProfile'
            profileName = argv[1]
            self.profile = Profile(profileName)
        else:
            self.action = 'invalidArgs'


def getCommandLineParser(app):
    return app.get('commandLineParser', createCommandLineParser(app))


def createCommandLineParser(app):
    return CommandLineParser()
