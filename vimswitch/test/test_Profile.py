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
