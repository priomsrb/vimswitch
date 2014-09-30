import unittest
from vimswitch.Profile import Profile


class TestProfile(unittest.TestCase):

    def test_getDirName_withSlashes_replacedByDot(self):
        profile = Profile('user/repo')
        self.assertEquals(profile.getDirName(), 'user.repo')
        profile = Profile('user/prefix.repo')
        self.assertEquals(profile.getDirName(), 'user.prefix.repo')

    def test_getDirName_withoutSlashes_isUnchanged(self):
        profile = Profile('repo')
        self.assertEquals(profile.getDirName(), 'repo')
        profile = Profile('prefix.repo')
        self.assertEquals(profile.getDirName(), 'prefix.repo')

    def test_equal(self):
        profile1 = Profile('user/repo')
        profile2 = Profile('user/repo')

        self.assertEqual(profile1, profile2)

    def test_notEqual(self):
        self.assertNotEqual(Profile('user/repo1'), Profile('user/repo2'))
        self.assertNotEqual(Profile('user/repo1'), None)
        self.assertNotEqual(None, Profile('user/repo2'))
