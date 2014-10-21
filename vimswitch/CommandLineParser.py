import argparse
from .Profile import Profile


class CommandLineParser:
    def __init__(self):
        self.action = ''
        self.profile = None
        self.errorMessage = ''
        self.helpText = ''

    def parse(self, argv):
        parser = self._createParser()
        self.helpText = parser.format_help()

        argv = argv[1:]  # Remove the program name from the arguments
        arguments = parser.parse_args(argv)

        self._processArguments(parser, arguments, argv)

    def _createParser(self):
        parser = CustomArgumentParser(
            prog='vimswitch',
            description='A utility for switching between vim profiles.')
        parser.add_argument('profile', nargs='?')
        parser.add_argument('-u', '--update', action='store_true',
                            help='download profile again')
        parser.add_argument('-v', '--version', action='store_true',
                            help='show version')
        return parser

    def _processArguments(self, parser, arguments, argv):
        if parser.hasError:
            self.errorMessage = parser.errorMessage
            self.action = 'invalidArgs'
        elif arguments.version:
            self.action = 'showVersion'
        elif arguments.update:
            self.action = 'updateProfile'
            profileName = arguments.profile
            if profileName is None:
                self.profile = None
            else:
                self.profile = Profile(profileName)
        elif arguments.profile is not None:
            self.action = 'switchProfile'
            profileName = arguments.profile
            self.profile = Profile(profileName)
        elif len(argv) == 0:
            self.action = 'showCurrentProfile'


def getCommandLineParser(app):
    return app.get('commandLineParser', createCommandLineParser(app))


def createCommandLineParser(app):
    return CommandLineParser()


class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        argparse.ArgumentParser.__init__(self, *args, **kwargs)
        self.hasError = False
        self.errorMessage = ''

    def error(self, message):
        self.hasError = True
        self.errorMessage = message
        # Disable automatic exiting
        return

    def print_help(self, *args, **kwargs):
        # Disable automatic printing
        return

    def exit(self, *args, **kwargs):
        # Disable automatic exiting
        return
