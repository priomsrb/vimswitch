from .BaseTestCase import BaseTestCase
from vimswitch.Profile import Profile
from vimswitch.ProfileUrlResolver import getProfileUrl


class TestProfileUrlResolver(BaseTestCase):

    def test_getProfileUrl_convertsUserSlashRepo(self):
        profile = Profile('testuser/testrepo')

        url = getProfileUrl(profile)

        expectedUrl = 'https://github.com/testuser/testrepo/archive/master.zip'
        self.assertEqual(url, expectedUrl)
