import unittest
from vimswitch.Profile import Profile
from vimswitch.ProfileUrlResolver import getProfileUrl


class TestProfileUrlResolver(unittest.TestCase):

    def test_getProfileUrl_convertsUserSlashRepo(self):
        profile = Profile('testuser/testrepo')

        url = getProfileUrl(profile)

        expectedUrl = 'https://github.com/testuser/testrepo/archive/master.zip'
        self.assertEqual(url, expectedUrl)
