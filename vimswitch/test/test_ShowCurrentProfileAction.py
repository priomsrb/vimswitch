from .BaseTestCase import BaseTestCase
from functools import partial
from mock import patch
from vimswitch.Application import Application
from vimswitch.Profile import Profile
from vimswitch.ShowCurrentProfileAction import createShowCurrentProfileAction
from vimswitch.six import StringIO


class TestShowCurrentProfileAction(BaseTestCase):
    def setUp(self):
        self.app = Application()
        self.action = createShowCurrentProfileAction(self.app)

    @patch('sys.stdout', new_callable=StringIO)
    def test_execute_printsCurrentProfile(self, stdout):
        self.app.settings.currentProfile = Profile('test/vimrc')

        self.action.execute()

        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutContains('Current profile: test/vimrc')

    @patch('sys.stdout', new_callable=StringIO)
    def test_execute_currentProfileIsNone_printsNone(self, stdout):
        self.app.settings.currentProfile = None

        self.action.execute()

        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutContains('Current profile: None')
