from mock import MagicMock, patch
from vimswitch.Application import Application
from vimswitch.Profile import Profile
from vimswitch.Settings import getSettings
from vimswitch.SwitchProfileAction import SwitchProfileAction
from vimswitch.UpdateProfileAction import UpdateProfileAction
from vimswitch.six import StringIO
from .BaseTestCase import BaseTestCase


class TestUpdateProfileAction(BaseTestCase):
    def setUp(self):
        app = Application()
        self.settings = getSettings(app)
        self.switchProfileAction = MagicMock(SwitchProfileAction)
        self.updateProfileAction = UpdateProfileAction(self.settings, self.switchProfileAction)

    def test_execute_withProfile_updatesProfile(self):
        self.updateProfileAction.profile = Profile('test/vimrc')

        self.updateProfileAction.execute()

        self.assertTrue(self.switchProfileAction.execute.called)
        self.assertEqual(self.switchProfileAction.profile, Profile('test/vimrc'))
        self.assertEqual(self.switchProfileAction.update, True)

    def test_execute_withoutProfile_updatesCurrentProfile(self):
        self.settings.currentProfile = Profile('test/currentProfile')
        self.updateProfileAction.profile = None

        self.updateProfileAction.execute()

        self.assertTrue(self.switchProfileAction.execute.called)
        self.assertEqual(self.switchProfileAction.profile, Profile('test/currentProfile'))
        self.assertEqual(self.switchProfileAction.update, True)

    @patch('sys.stdout', new_callable=StringIO)
    def test_execute_withDefaultProfile_printError(self, stdout):
        self.updateProfileAction.profile = Profile('default')

        self.updateProfileAction.execute()

        self.assertFalse(self.switchProfileAction.execute.called)
        self.assertEqual(self.updateProfileAction.exitCode, -1)
        self.assertStdout(stdout, 'Cannot update default profile')
