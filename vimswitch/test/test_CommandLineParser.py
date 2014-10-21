from .BaseTestCase import BaseTestCase
from vimswitch.CommandLineParser import CommandLineParser
from vimswitch.Profile import Profile


class TestCommandLineParser(BaseTestCase):

    def setUp(self):
        self.commandLineParser = CommandLineParser()

    def test_parse_emptyArgs_setsShowCurrentProfileAction(self):
        argv = './vimswitch'.split()
        self.commandLineParser.parse(argv)
        self.assertEqual(self.commandLineParser.action, 'showCurrentProfile')

    def test_parse_setsSwitchProfileAction(self):
        argv = './vimswitch test/vimrc'.split()

        self.commandLineParser.parse(argv)

        self.assertEqual(self.commandLineParser.action, 'switchProfile')
        self.assertEqual(self.commandLineParser.profile, Profile('test/vimrc'))

    def test_parse_updateProfileAction(self):
        argv = './vimswitch --update test/vimrc'.split()

        self.commandLineParser.parse(argv)

        self.assertEqual(self.commandLineParser.action, 'updateProfile')
        self.assertEqual(self.commandLineParser.profile, Profile('test/vimrc'))

    def test_parse_updateWithoutProfile_setProfileToNone(self):
        argv = './vimswitch --update'.split()

        self.commandLineParser.parse(argv)

        self.assertEqual(self.commandLineParser.action, 'updateProfile')
        self.assertEqual(self.commandLineParser.profile, None)

    def test_parse_showVersionAction(self):
        argv = './vimswitch --version'.split()
        self.commandLineParser.parse(argv)
        self.assertEqual(self.commandLineParser.action, 'showVersion')

    def test_parse_tooManyArgs_setsErrorMessage(self):
        argv = './vimswitch test/vimrc foo'.split()

        self.commandLineParser.parse(argv)

        self.assertEqual(self.commandLineParser.action, 'invalidArgs')
        self.assertEqual(self.commandLineParser.errorMessage, 'unrecognized arguments: foo')

    def test_parse_invalidFlag_setsErrorMessage(self):
        argv = './vimswitch --foo test/vimrc'.split()

        self.commandLineParser.parse(argv)

        self.assertEqual(self.commandLineParser.action, 'invalidArgs')
        self.assertEqual(self.commandLineParser.errorMessage, 'unrecognized arguments: --foo')
