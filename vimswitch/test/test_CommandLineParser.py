from .BaseTestCase import BaseTestCase
from vimswitch.CommandLineParser import CommandLineParser
from vimswitch.Profile import Profile


class TestCommandLineParser(BaseTestCase):

    def setUp(self):
        self.commandLineParser = CommandLineParser()

    def test_parse_emptyArgs_setsShowCurrentProfileAction(self):
        argv = ['./vimswitch']
        self.commandLineParser.parse(argv)
        self.assertEqual(self.commandLineParser.action, 'showCurrentProfile')

    def test_parse_setsSwitchProfileAction(self):
        argv = ['./vimswitch', 'test/vimrc']

        self.commandLineParser.parse(argv)

        self.assertEqual(self.commandLineParser.action, 'switchProfile')
        self.assertEqual(self.commandLineParser.profile, Profile('test/vimrc'))

    def test_parse_tooManyArgs_setsErrorMessage(self):
        argv = ['./vimswitch', 'test/vimrc', 'foo']

        self.commandLineParser.parse(argv)

        self.assertEqual(self.commandLineParser.action, 'invalidArgs')
