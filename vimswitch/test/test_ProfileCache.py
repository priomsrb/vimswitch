import unittest
import Stubs
import os
from mock import MagicMock
from vimswitch.ProfileCache import ProfileCache
from vimswitch.Profile import Profile


class TestProfileCache(unittest.TestCase):

    def setUp(self):
        self.settings = Stubs.SettingsStub()
        self.diskIo = Stubs.DiskIoStub()
        self.profileCache = ProfileCache(self.settings, self.diskIo)
        self.testProfile = Profile('test/vimrc')

    # ProfileCache.contains

    def test_contains_whenDirExists_returnsTrue(self):
        self.diskIo.dirExists.return_value = True
        result = self.profileCache.contains(self.testProfile)
        self.assertTrue(result)

    def test_contains_whenDirDoesNotExist_returnsFalse(self):
        self.diskIo.dirExists.return_value = False
        result = self.profileCache.contains(self.testProfile)
        self.assertFalse(result)

    def test_contains_usesGetLocation(self):
        self.profileCache.getLocation = MagicMock()
        self.profileCache.contains(self.testProfile)
        self.assertTrue(self.profileCache.getLocation.called)

    # ProfileCache.delete

    def test_delete_deletesProfile(self):
        # TODO: Write test. Would be easier if this was a filesystem test
        pass

    # ProfileCache.getLocation

    def test_getLocation(self):
        self.settings.cachePath = '/foo/bar/cache'
        profile = Profile('test/vimrc')
        result = self.profileCache.getLocation(profile)
        self.assertEquals(result, os.path.normpath('/foo/bar/cache/test.vimrc'))

    # ProfileCache.createEmptyProfile

    def test_createEmptyProfile_profileDoesNotExist_createsProfileDir(self):
        self.settings.cachePath = '/foo/bar/cache'
        profile = Profile('default')
        self.profileCache.createEmptyProfile(profile)
        self.diskIo.createDir.assert_called_with(os.path.normpath('/foo/bar/cache/default'))
