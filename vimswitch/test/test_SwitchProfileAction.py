from .FakeFileDownloader import createFakeFileDownloader
from .FileSystemTestCase import FileSystemTestCase
from mock import MagicMock, patch
from vimswitch.Application import Application
from vimswitch.Profile import Profile
from vimswitch.Settings import Settings
from vimswitch.SwitchProfileAction import createSwitchProfileAction
from vimswitch.six import StringIO
import os


class TestSwitchProfileAction(FileSystemTestCase):

    def setUp(self):
        FileSystemTestCase.setUp(self)
        self.app = Application()
        self.app.settings = Settings(self.getWorkingDir())
        self.app.fileDownloader = createFakeFileDownloader(self.app, self.getDataPath('fake_internet'))
        self.switchProfileAction = createSwitchProfileAction(self.app)
        self.app.diskIo.createDirWithParents(self.app.settings.cachePath)
        self.app.diskIo.createDirWithParents(self.app.settings.downloadsPath)
        self.profile = Profile('test/vimrc')

    def test_switchToProfile_defaultProfileDoesNotExist_createsDefaultProfile(self):
        self.switchProfileAction.profile = self.profile

        self.switchProfileAction.execute()

        defaultProfile = self.app.settings.defaultProfile
        self.assertTrue(self.app.profileCache.contains(defaultProfile))

    def test_switchToProfile_profileNotInCache_downloadsProfile(self):
        self.switchProfileAction.profile = self.profile
        self.switchProfileAction.execute()
        self.assertTrue(self.app.profileCache.contains(self.profile))

    def test_switchToProfile_profileInCache_doesNotDownloadProfile(self):
        self.app.fileDownloader.download = MagicMock(side_effect=AssertionError('Profile should not be downloaded'))
        self.app.profileCache.createEmptyProfile(self.profile)
        self.switchProfileAction.profile = self.profile

        self.switchProfileAction.execute()

    def test_switchToProfile_copiesProfileToHome(self):
        self.switchProfileAction.profile = self.profile

        self.switchProfileAction.execute()

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
        self.switchProfileAction.profile = self.profile

        self.switchProfileAction.execute()

        defaultProfile = self.app.settings.defaultProfile
        cachedVimrcPath = os.path.join(self.app.profileCache.getProfileLocation(defaultProfile), '.vimrc')
        expectedVimrc = '" default vimrc'
        actualVimrc = self.app.diskIo.getFileContents(cachedVimrcPath)
        self.assertEqual(expectedVimrc, actualVimrc)
        cachedVimDirPath = os.path.join(self.app.profileCache.getProfileLocation(defaultProfile), '.vim')
        self.assertTrue(self.app.diskIo.dirExists(cachedVimDirPath))

    def test_switchToProfile_savesProfileChangesToCache(self):
        self.switchProfileAction.profile = self.profile
        self.switchProfileAction.execute()
        # Now we make changes to the profile
        vimrcPath = self.getTestPath('.vimrc')
        vimDirPath = self.getTestPath('.vim')
        self.app.diskIo.createFile(vimrcPath, '" updated vimrc')  # Edit file
        self.app.diskIo.deleteDir(vimDirPath)  # Delete dir
        defaultProfile = self.app.settings.defaultProfile
        self.switchProfileAction.profile = defaultProfile

        self.switchProfileAction.execute()

        # Assert .vimrc updated
        cachedVimrcPath = os.path.join(self.app.profileCache.getProfileLocation(self.profile), '.vimrc')
        expectedVimrc = '" updated vimrc'
        actualVimrc = self.app.diskIo.getFileContents(cachedVimrcPath)
        self.assertEqual(expectedVimrc, actualVimrc)
        # Assert .vim deleted
        cachedVimDirPath = os.path.join(self.app.profileCache.getProfileLocation(defaultProfile), '.vim')
        self.assertFalse(self.app.diskIo.dirExists(cachedVimDirPath))

    def test_switchToProfile_updateFlagSet_updatesCachedProfile(self):
        # Do an initial download of the profile
        self.switchProfileAction.profile = self.profile
        self.switchProfileAction.execute()
        # Update the profile on the internet by using the version at fake_internet2
        self.app.fileDownloader.root = self.getDataPath('fake_internet2')
        self.switchProfileAction.update = True
        self.switchProfileAction.profile = self.profile

        self.switchProfileAction.execute()

        self.assertFileContents('.vimrc', '" updated vimrc data')
        self.assertFileContents('.vimswitch/profiles/test.vimrc/.vimrc', '" updated vimrc data')
        vimDirPath = self.getTestPath('.vim')
        self.assertTrue(self.app.diskIo.dirExists(vimDirPath))

    def test_switchToProfile_setsCurrentProfile(self):
        self.assertNotEqual(self.app.settings.currentProfile, self.profile)
        self.switchProfileAction.profile = self.profile

        self.switchProfileAction.execute()

        self.assertEqual(self.app.settings.currentProfile, self.profile)

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchToProfile_prints(self, stdout):
        self.switchProfileAction.profile = self.profile

        self.switchProfileAction.execute()

        self.assertStdout(stdout, """
            Saving profile: default
            Downloading profile from https://github.com/test/vimrc/archive/master.zip
            Switched to profile: test/vimrc
        """)

    # Helpers

    def assertFileContents(self, path, expectedContents):
        diskIo = self.app.diskIo
        path = self.getTestPath(path)
        actualContents = diskIo.getFileContents(path)
        self.assertEqual(actualContents, expectedContents)
