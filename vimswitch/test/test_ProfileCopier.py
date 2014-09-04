import unittest
import Stubs
from mock import MagicMock
from vimswitch.Profile import Profile
from vimswitch.ProfileCache import ProfileCache
from vimswitch.ProfileCopier import ProfileCopier


class TestProfileCopier(unittest.TestCase):
    def setUp(self):
        self.profile = Profile('test/vimrc')
        self.settings = Stubs.SettingsStub()
        self.diskIo = Stubs.DiskIoStub()
        # We use the real ProfileCache (with stubbed dependencies) because
        # ProfileCache.getLocation gets called by ProfileCopier
        self.profileCache = ProfileCache(self.settings, self.diskIo)
        self.profileDataIo = Stubs.ProfileDataIoStub()
        self.profileCopier = ProfileCopier(self.settings, self.profileCache, self.profileDataIo)

    # ProfileCopier.copyToHome(profile)

    def test_copyToHome_deletesHomeData(self):
        self.profileCopier.copyToHome(self.profile)

        homePath = '/home/foo'
        self.profileDataIo.delete.assert_called_with(homePath)

    def test_copyToHome_deletesHomeDir_fromSettings(self):
        self.settings.getHomeDir.return_value = 'testHomeDir'

        self.profileCopier.copyToHome(self.profile)

        self.profileDataIo.delete.assert_called_with('testHomeDir')

    def test_copyToHome_copiesFromProfileToHome(self):
        self.profileCopier.copyToHome(self.profile)

        profilePath = '/home/foo/.vimswitch/test.vimrc'
        homePath = '/home/foo'
        self.profileDataIo.copy.assert_called_with(profilePath, homePath)

    def test_copyToHome_copiesFromCacheDir_fromSettings(self):
        self.settings.getCacheDir.return_value = 'testCacheDir'

        self.profileCopier.copyToHome(self.profile)

        profilePath = 'testCacheDir/test.vimrc'
        homePath = '/home/foo'
        self.profileDataIo.copy.assert_called_with(profilePath, homePath)

    def test_copyToHome_copiesToHomeDir_fromSettings(self):
        self.settings.getHomeDir.return_value = 'testHomeDir'

        self.profileCopier.copyToHome(self.profile)

        profilePath = '/home/foo/.vimswitch/test.vimrc'
        homePath = 'testHomeDir'
        self.profileDataIo.copy.assert_called_with(profilePath, homePath)

    # ProfileCopier.copyFromHome

    def test_copyfromHome_profileInCache_doNotCreateEmptyProfile(self):
        self.profileCache.contains = MagicMock(spec=ProfileCache.contains, return_value=True)
        self.profileCache.createEmptyProfile = MagicMock(ProfileCache.createEmptyProfile)

        self.profileCopier.copyFromHome(self.profile)

        self.assertFalse(self.profileCache.createEmptyProfile.called)

    def test_copyfromHome_profileNotInCache_createEmptyProfile(self):
        self.profileCache.contains = MagicMock(spec=ProfileCache.contains, return_value=False)
        self.profileCache.createEmptyProfile = MagicMock(ProfileCache.createEmptyProfile)

        self.profileCopier.copyFromHome(self.profile)

        self.assertTrue(self.profileCache.createEmptyProfile.called)

    def test_copyfromHome_deletesProfileDir(self):
        self.profileCopier.copyFromHome(self.profile)

        profilePath = '/home/foo/.vimswitch/test.vimrc'
        self.profileDataIo.delete.assert_called_with(profilePath)

    def test_copyfromHome_copiesFromHomeToProfile(self):
        self.profileCopier.copyFromHome(self.profile)

        homePath = '/home/foo'
        profilePath = '/home/foo/.vimswitch/test.vimrc'
        self.profileDataIo.copy.assert_called_with(homePath, profilePath)

    def test_copyfromHome_copiesFromHomeDir_fromSettings(self):
        self.settings.getHomeDir.return_value = 'testHomeDir'
        self.profileCopier.copyFromHome(self.profile)

        homePath = 'testHomeDir'
        profilePath = '/home/foo/.vimswitch/test.vimrc'
        self.profileDataIo.copy.assert_called_with(homePath, profilePath)

    def test_copyfromHome_copiesToCacheDir_fromSettings(self):
        self.settings.getCacheDir.return_value = 'testCacheDir'
        self.profileCopier.copyFromHome(self.profile)

        homePath = '/home/foo'
        profilePath = 'testCacheDir/test.vimrc'
        self.profileDataIo.copy.assert_called_with(homePath, profilePath)
