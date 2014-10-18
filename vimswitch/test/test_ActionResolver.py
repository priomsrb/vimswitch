from .BaseTestCase import BaseTestCase
from .Stubs import DiskIoStub
from mock import patch
from vimswitch.ActionResolver import ActionResolver
from vimswitch.Application import Application
from vimswitch.CommandLineParser import CommandLineParser
from vimswitch.Profile import Profile


class TestActionResolver(BaseTestCase):

    def setUp(self):
        app = Application()
        app.diskIo = DiskIoStub()  # Fake all disk operations
        self.commandLineParser = CommandLineParser()
        self.actionResolver = ActionResolver(app, self.commandLineParser)
        self.profile = Profile('test/vimrc')

    @patch('vimswitch.SwitchProfileAction.SwitchProfileAction')
    def test_doActions_resolvesSwitchProfileAction(self, mock):
        self.commandLineParser.action = 'switchProfile'
        self.commandLineParser.profile = self.profile

        self.actionResolver.doActions()

        switchProfileAction = mock.return_value
        switchProfileAction.switchToProfile.assert_called_with(self.profile)

    @patch('vimswitch.UpdateProfileAction.UpdateProfileAction')
    def test_doActions_resolvesUpdateProfileAction(self, mock):
        self.commandLineParser.action = 'updateProfile'
        self.commandLineParser.profile = self.profile

        self.actionResolver.doActions()

        updateProfileAction = mock.return_value
        self.assertEqual(updateProfileAction.profile, self.profile)
        self.assertTrue(updateProfileAction.execute.called)

    @patch('vimswitch.ActionResolver.createShowCurrentProfileAction')
    def test_doActions_resolvesShowCurrentProfileAction(self, mock):
        self.commandLineParser.action = 'showCurrentProfile'

        self.actionResolver.doActions()

        showCurrentProfileAction = mock.return_value
        self.assertTrue(showCurrentProfileAction.execute.called)

    @patch('vimswitch.ActionResolver.InvalidArgsAction')
    def test_doActions_resolvesInvalidArgsAction(self, mock):
        self.commandLineParser.action = 'invalidArgs'
        self.commandLineParser.errorMessage = 'testErrorMessage'
        self.commandLineParser.helpText = 'testHelpText'

        self.actionResolver.doActions()

        invalidArgsAction = mock
        invalidArgsAction.assert_called_with('testErrorMessage', 'testHelpText')

    @patch('vimswitch.ActionResolver.InvalidArgsAction')
    def test_doActions_unknownAction_executesInvalidArgsAction(self, mock):
        self.commandLineParser.action = 'unknownAction'

        self.actionResolver.doActions()

        invalidArgsAction = mock.return_value
        self.assertTrue(invalidArgsAction.execute.called)
