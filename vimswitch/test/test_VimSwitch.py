from .FakeFileDownloader import createFakeFileDownloader
from .FileSystemTestCase import FileSystemTestCase
from vimswitch.Settings import Settings
from mock import patch
from vimswitch.Application import Application
from vimswitch.VimSwitch import VimSwitch
from vimswitch.six import StringIO
from functools import partial


class TestVimSwitch(FileSystemTestCase):

    def setUp(self):
        FileSystemTestCase.setUp(self)
        self.resetApplication()

    def resetApplication(self):
        """
        Resets the state of the application. If you need to call
        vimswitch.main() multiple times in a test, make sure to call this method
        after every vimswitch.main().
        """
        self.app = Application()
        self.app.settings = Settings(self.getWorkingDir())
        self.app.fileDownloader = createFakeFileDownloader(self.app, self.getDataPath('fake_internet'))
        self.vimSwitch = VimSwitch(self.app)
        self.vimSwitch.raiseExceptions = True

    def test_switchProfile_createsApplicationDirs(self):
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0)
        # Assert application dirs exist
        settings = self.app.settings
        diskIo = self.app.diskIo
        self.assertTrue(diskIo.dirExists(settings.configPath))
        self.assertTrue(diskIo.dirExists(settings.cachePath))
        self.assertTrue(diskIo.dirExists(settings.downloadsPath))

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_switchToRemoteProfile(self, stdout):
        self.copyDataToWorkingDir('home/.vimrc', '.vimrc')
        self.copyDataToWorkingDir('home/.vim', '.vim')
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0)
        # Assert default profile is created
        diskIo = self.app.diskIo
        defaultVimrcFilePath = self.getTestPath('.vimswitch/default/.vimrc')
        defaultVimDirPath = self.getTestPath('.vimswitch/default/.vim')
        defaultVimrcContents = diskIo.getFileContents(defaultVimrcFilePath)
        self.assertEqual(defaultVimrcContents, '" home vimrc data')
        self.assertTrue(diskIo.dirExists(defaultVimDirPath))
        # Assert home profile is replaced by downloaded profile
        downloadedVimrcFilePath = self.getTestPath('.vimrc')
        downloadedVimDirPath = self.getTestPath('.vim')
        downloadedVimrcContents = diskIo.getFileContents(downloadedVimrcFilePath)
        self.assertEqual(downloadedVimrcContents, '" test vimrc data')
        self.assertTrue(diskIo.dirExists(downloadedVimDirPath))
        # Assert stdout
        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutContains('Downloading profile from https://github.com/test/vimrc/archive/master.zip')
        assertStdoutContains('Switched to profile: test/vimrc')

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_switchToNonExistantProfile_showsError(self, stdout):
        self.copyDataToWorkingDir('home/.vimrc', '.vimrc')
        self.copyDataToWorkingDir('home/.vim', '.vim')
        argv = ['./vimswitch', 'non_existant_profile']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, -1, stdout.getvalue())
        # Assert home profile is unchanged
        downloadedVimrcFilePath = self.getTestPath('.vimrc')
        downloadedVimDirPath = self.getTestPath('.vim')
        diskIo = self.app.diskIo
        downloadedVimrcContents = diskIo.getFileContents(downloadedVimrcFilePath)
        self.assertEqual(downloadedVimrcContents, '" home vimrc data')
        self.assertTrue(diskIo.dirExists(downloadedVimDirPath))
        # Assert stdout
        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutContains('Downloading profile from https://github.com/non_existant_profile/archive/master.zip')
        assertStdoutContains('Error:')
        assertStdoutContains('404 File not found')

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_switchToAnotherProfile(self, stdout):
        argv1 = ['./vimswitch', 'test/vimrc']
        argv2 = ['./vimswitch', 'test2/vimrc']
        # Switch to an initial profile
        self.vimSwitch.main(argv1)
        self.resetApplication()
        # Clear stdout from previous calls
        stdout.truncate(0)
        stdout.seek(0)

        # Now switch to another profile
        exitCode = self.vimSwitch.main(argv2)

        self.assertEqual(exitCode, 0, stdout.getvalue())
        # Assert current profile is now test2/vimrc
        diskIo = self.app.diskIo
        currentVimrcFilePath = self.getTestPath('.vimrc')
        currentVimDirPath = self.getTestPath('.vim')
        currentVimrcContents = diskIo.getFileContents(currentVimrcFilePath)
        self.assertEqual(currentVimrcContents, '" test2 vimrc data')
        self.assertTrue(diskIo.dirExists(currentVimDirPath))
        # Assert stdout
        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutContains('Downloading profile from https://github.com/test2/vimrc/archive/master.zip')
        assertStdoutContains('Switched to profile: test2/vimrc')

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_switchToCachedProfile(self, stdout):
        argv1 = ['./vimswitch', 'test/vimrc']
        argv2 = ['./vimswitch', 'test2/vimrc']
        # Download 2 profiles
        self.vimSwitch.main(argv1)
        self.resetApplication()
        self.vimSwitch.main(argv2)
        self.resetApplication()
        # Clear stdout from previous calls
        stdout.truncate(0)
        stdout.seek(0)

        # Switch back to the first profile
        exitCode = self.vimSwitch.main(argv1)

        self.assertEqual(exitCode, 0, stdout.getvalue())
        # Assert current profile is now test/vimrc
        diskIo = self.app.diskIo
        currentVimrcFilePath = self.getTestPath('.vimrc')
        currentVimDirPath = self.getTestPath('.vim')
        currentVimrcContents = diskIo.getFileContents(currentVimrcFilePath)
        self.assertEqual(currentVimrcContents, '" test vimrc data')
        self.assertTrue(diskIo.dirExists(currentVimDirPath))
        # Assert stdout
        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutNotContains = partial(self.assertNotRegex, stdout.getvalue())
        assertStdoutNotContains('Downloading')
        assertStdoutContains('Switched to profile: test/vimrc')

    def test_switchProfile_switchFromEmptyDefaultProfile(self):
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0)
        # Assert default profile is created and empty
        diskIo = self.app.diskIo
        defaultProfilePath = self.getTestPath('.vimswitch/default')
        self.assertTrue(diskIo.dirExists(defaultProfilePath))
        self.assertTrue(diskIo.isDirEmpty(defaultProfilePath))
        # Assert home profile is replaced by downloaded profile
        downloadedVimrcFilePath = self.getTestPath('.vimrc')
        downloadedVimDirPath = self.getTestPath('.vim')
        downloadedVimrcContents = diskIo.getFileContents(downloadedVimrcFilePath)
        self.assertEqual(downloadedVimrcContents, '" test vimrc data')
        self.assertTrue(diskIo.dirExists(downloadedVimDirPath))

    def test_switchProfile_switchToEmptyDefaultProfile(self):
        argv1 = ['./vimswitch', 'test/vimrc']
        argv2 = ['./vimswitch', 'default']
        # Switch to non-default profile
        self.vimSwitch.main(argv1)
        self.resetApplication()

        # Now switch back to default profile
        exitCode = self.vimSwitch.main(argv2)

        self.assertEqual(exitCode, 0)
        # Assert home profile is now empty
        diskIo = self.app.diskIo
        homeVimrcFilePath = self.getTestPath('.vimrc')
        homeVimDirPath = self.getTestPath('.vim')
        self.assertFalse(diskIo.anyExists(homeVimrcFilePath))
        self.assertFalse(diskIo.anyExists(homeVimDirPath))

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_switchFromReadOnlyProfileData(self, stdout):
        diskIo = self.app.diskIo
        self.copyDataToWorkingDir('home/.vimrc', '.vimrc')
        self.copyDataToWorkingDir('home/.vim', '.vim')
        dummyPluginPath = self.getTestPath('.vim/plugin/dummy_plugin.vim')
        diskIo.setReadOnly(dummyPluginPath, True)
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0, stdout.getvalue())
        # Assert default profile is created
        defaultVimrcFilePath = self.getTestPath('.vimswitch/default/.vimrc')
        defaultVimDirPath = self.getTestPath('.vimswitch/default/.vim')
        defaultVimrcContents = diskIo.getFileContents(defaultVimrcFilePath)
        defaultDummyPluginPath = self.getTestPath('.vimswitch/default/.vim/plugin/dummy_plugin.vim')
        defaultDummyPluginContents = diskIo.getFileContents(defaultDummyPluginPath)
        self.assertEqual(defaultVimrcContents, '" home vimrc data')
        self.assertEqual(defaultDummyPluginContents, '" dummy home vim plugin')
        self.assertTrue(diskIo.dirExists(defaultVimDirPath))
        # Assert home profile is replaced by downloaded profile
        downloadedVimrcFilePath = self.getTestPath('.vimrc')
        downloadedVimDirPath = self.getTestPath('.vim')
        downloadedVimrcContents = diskIo.getFileContents(downloadedVimrcFilePath)
        self.assertEqual(downloadedVimrcContents, '" test vimrc data')
        self.assertTrue(diskIo.dirExists(downloadedVimDirPath))
        # Assert home profile no longer contains read-only file
        oldDummyPluginPath = self.getTestPath('.vim/plugin/dummy_plugin.vim')
        self.assertFalse(diskIo.anyExists(oldDummyPluginPath))
        # Assert stdout
        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutContains('Downloading profile from https://github.com/test/vimrc/archive/master.zip')
        assertStdoutContains('Switched to profile: test/vimrc')

    def test_switchProfile_savesChangesToCurrentProfile(self):
        self.copyDataToWorkingDir('home/.vimrc', '.vimrc')
        self.copyDataToWorkingDir('home/.vim', '.vim')
        argv1 = ['./vimswitch', 'test/vimrc']
        argv2 = ['./vimswitch', 'default']
        self.vimSwitch.main(argv1)
        self.resetApplication()
        homeVimrcFilePath = self.getTestPath('.vimrc')
        homeVimDirPath = self.getTestPath('.vim')
        diskIo = self.app.diskIo
        # Make changes to the test/vimrc profile
        diskIo.createFile(homeVimrcFilePath, '" updated vimrc data')
        diskIo.deleteDir(homeVimDirPath)

        self.vimSwitch.main(argv2)

        # Assert .vimrc changes saved
        cachedVimrcFilePath = self.getTestPath('.vimswitch/test.vimrc/.vimrc')
        cachedVimrcContents = diskIo.getFileContents(cachedVimrcFilePath)
        self.assertEqual(cachedVimrcContents, '" updated vimrc data')
        # Assert .vim dir deleted
        cachedVimDirPath = self.getTestPath('.vimswitch/test.vimrc/.vim')
        self.assertFalse(diskIo.anyExists(cachedVimDirPath))
        # TODO: Assert stdout

    def test_switchProfile_ignoresNonProfileFiles(self):
        # We will check that the following files and dirs still exist after
        # switching profiles
        filePaths = [
            'test'
            'test.txt'
            '.test'
            '.vimperatorrc'
            '.viminfo'
            '_viminfo'
        ]
        dirPaths = [
            'testDir'
            'testDir.txt'
            '.testDir'
            '.vimperator'
        ]
        diskIo = self.app.diskIo
        for filePath in filePaths:
            diskIo.createFile(self.getTestPath(filePath), 'test content')
        for dirPath in dirPaths:
            diskIo.createDir(self.getTestPath(dirPath))
        self.copyDataToWorkingDir('home/.vimrc', '_vimrc')
        self.copyDataToWorkingDir('home/.vim', '_vim')
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0)
        # Assert all the non-profile files and dirs still exist
        for filePath in filePaths:
            content = diskIo.getFileContents(self.getTestPath(filePath))
            self.assertEqual(content, 'test content')
        for dirPath in dirPaths:
            path = self.getTestPath(dirPath)
            self.assertTrue(diskIo.dirExists(path))

    def test_switchProfile_switchFromWindowsProfile_movesWindowsProfileDataToCache(self):
        self.copyDataToWorkingDir('home/.vimrc', '_vimrc')
        self.copyDataToWorkingDir('home/.vim', '_vim')
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0)
        # Assert windows profile files are deleted
        diskIo = self.app.diskIo
        windowsVimrcFilePath = self.getTestPath('_vimrc')
        windowsVimDirPath = self.getTestPath('_vim')
        self.assertFalse(diskIo.anyExists(windowsVimrcFilePath))
        self.assertFalse(diskIo.anyExists(windowsVimDirPath))
        # Assert windows profile moved to cache
        cachedVimrcFilePath = self.getTestPath('.vimswitch/default/_vimrc')
        cachedVimDirPath = self.getTestPath('.vimswitch/default/_vim')
        cachedVimrcContents = diskIo.getFileContents(cachedVimrcFilePath)
        self.assertEqual(cachedVimrcContents, '" home vimrc data')
        self.assertTrue(diskIo.dirExists(cachedVimDirPath))
        # Assert home profile is replaced by downloaded profile
        downloadedVimrcFilePath = self.getTestPath('.vimrc')
        downloadedVimDirPath = self.getTestPath('.vim')
        downloadedVimrcContents = diskIo.getFileContents(downloadedVimrcFilePath)
        self.assertEqual(downloadedVimrcContents, '" test vimrc data')
        self.assertTrue(diskIo.dirExists(downloadedVimDirPath))

    @patch('sys.stdout', new_callable=StringIO)
    def test_noArguments_showsCurrentProfile(self, stdout):
        argv1 = ['./vimswitch', 'test/vimrc']
        argv2 = ['./vimswitch']
        self.vimSwitch.main(argv1)  # Sets current profile to test/vimrc
        self.resetApplication()
        # Clear stdout from previous calls
        stdout.truncate(0)
        stdout.seek(0)

        exitCode = self.vimSwitch.main(argv2)

        self.assertEqual(exitCode, 0, stdout.getvalue())
        # Assert stdout
        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutContains('Current profile: test/vimrc')

    @patch('sys.stdout', new_callable=StringIO)
    def test_noArgumentsAndNoCurrentProfile_showsCurrentProfileIsNone(self, stdout):
        argv = ['./vimswitch']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0, stdout.getvalue())
        # Assert stdout
        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutContains('Current profile: None')

    @patch('sys.stdout', new_callable=StringIO)
    def test_tooManyArgs_showsErrorMessage(self, stdout):
        argv = ['./vimswitch', 'test/vimrc', 'extra_argument']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, -1, stdout.getvalue())
        # Assert stdout
        assertStdoutContains = partial(self.assertRegexpMatches, stdout.getvalue())
        assertStdoutContains('Invalid arguments. Use `vimswitch myuser/myrepo` to switch profiles.')
