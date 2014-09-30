import os
from vimswitch.Settings import Settings
from vimswitch.DiskIo import DiskIo
from vimswitch.ProfileCache import ProfileCache
from vimswitch.Profile import Profile
from .FileSystemTestCase import FileSystemTestCase


class TestProfileCache(FileSystemTestCase):

    def setUp(self):
        FileSystemTestCase.setUp(self)
        self.diskIo = DiskIo()
        self.settings = Settings(self.getWorkingDir())
        self.diskIo.createDirWithParents(self.settings.cachePath)
        self.profileCache = ProfileCache(self.settings, self.diskIo)
        self.testProfile = Profile('test/vimrc')

    # ProfileCache.contains

    def test_contains_whenDirExists_returnsTrue(self):
        profileDir = self.getTestPath('.vimswitch/test.vimrc')
        self.diskIo.createDir(profileDir)

        result = self.profileCache.contains(self.testProfile)

        self.assertTrue(result)

    def test_contains_whenDirDoesNotExist_returnsFalse(self):
        result = self.profileCache.contains(self.testProfile)
        self.assertFalse(result)

    # ProfileCache.delete

    def test_delete_deletesProfile(self):
        profileDir = self.getTestPath('.vimswitch/test.vimrc')
        vimrcFilePath = self.getTestPath('.vimswitch/test.vimrc/.vimrc')
        self.diskIo.createDir(profileDir)
        self.diskIo.createFile(vimrcFilePath, 'test data')

        self.profileCache.delete(self.testProfile)

        self.assertFalse(self.profileCache.contains(self.testProfile))

    # ProfileCache.getProfileLocation

    def test_getProfileLocation(self):
        self.settings.cachePath = '/foo/bar/cache'
        profile = Profile('test/vimrc')
        result = self.profileCache.getProfileLocation(profile)
        self.assertEquals(result, os.path.normpath('/foo/bar/cache/test.vimrc'))

    # ProfileCache.createEmptyProfile

    def test_createEmptyProfile_profileDoesNotExist_createsProfileDir(self):
        profile = Profile('default')

        self.profileCache.createEmptyProfile(profile)

        profileDir = self.getTestPath('.vimswitch/default')
        self.assertTrue(self.diskIo.dirExists(profileDir))
