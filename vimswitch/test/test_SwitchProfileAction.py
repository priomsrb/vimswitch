from .FakeFileDownloader import createFakeFileDownloader
from .FileSystemTestCase import FileSystemTestCase
from vimswitch.six import StringIO
from .Stubs import SettingsWorkingDirStub
from mock import MagicMock, patch
from vimswitch.Application import Application
from vimswitch.Profile import Profile
from vimswitch.SwitchProfileAction import getSwitchProfileAction
import os


class TestSwitchProfileAction(FileSystemTestCase):

    def setUp(self):
        FileSystemTestCase.setUp(self)
        self.app = Application()
        self.app.settings = SettingsWorkingDirStub(self.getWorkingDir())
        self.app.fileDownloader = createFakeFileDownloader(self.app, self.getDataPath('fake_internet'))
        self.switchProfileAction = getSwitchProfileAction(self.app)
        self.app.diskIo.createDirWithParents(self.app.settings.cachePath)
        self.app.diskIo.createDirWithParents(self.app.settings.downloadsPath)
        self.profile = Profile('test/vimrc')

    def test_switchToProfile_defaultProfileDoesNotExist_createsDefaultProfile(self):
        self.switchProfileAction.switchToProfile(self.profile)

        defaultProfile = self.app.settings.defaultProfile
        self.assertTrue(self.app.profileCache.contains(defaultProfile))

    def test_switchToProfile_profileNotInCache_downloadsProfile(self):
        self.switchProfileAction.switchToProfile(self.profile)
        self.assertTrue(self.app.profileCache.contains(self.profile))

    def test_switchToProfile_profileInCache_doesNotDownloadProfile(self):
        self.app.fileDownloader.download = MagicMock(side_effect=AssertionError('Profile should not be downloaded'))
        self.app.profileCache.createEmptyProfile(self.profile)

        self.switchProfileAction.switchToProfile(self.profile)

    def test_switchToProfile_copiesProfileToHome(self):
        self.switchProfileAction.switchToProfile(self.profile)

        expectedVimrc = '" test vimrc data'
        actualVimrc = self.app.diskIo.getFileContents(self.getTestPath('.vimrc'))
        self.assertEqual(expectedVimrc, actualVimrc)
        vimDirPath = self.getTestPath('.vim')
        self.assertTrue(self.app.diskIo.dirExists(vimDirPath))

    def test_switchToProfile_copiesHomeToCache(self):
        vimrcPath = self.getTestPath('.vimrc')
        vimDirPath = self.getTestPath('.vim')
        self.app.diskIo.createFile(vimrcPath, '" default vimrc')
        self.app.diskIo.createDir(vimDirPath)

        self.switchProfileAction.switchToProfile(self.profile)

        defaultProfile = self.app.settings.defaultProfile
        cachedVimrcPath = os.path.join(self.app.profileCache.getLocation(defaultProfile), '.vimrc')
        expectedVimrc = '" default vimrc'
        actualVimrc = self.app.diskIo.getFileContents(cachedVimrcPath)
        self.assertEqual(expectedVimrc, actualVimrc)
        cachedVimDirPath = os.path.join(self.app.profileCache.getLocation(defaultProfile), '.vim')
        self.assertTrue(self.app.diskIo.dirExists(cachedVimDirPath))

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchToProfile_prints(self, stdout):
        self.switchProfileAction.switchToProfile(self.profile)

        expectedOutput = 'Switched to profile: test/vimrc'
        self.assertRegexpMatches(stdout.getvalue(), expectedOutput)
