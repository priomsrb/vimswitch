from .FakeFileDownloader import createFakeFileDownloader
from .FileSystemTestCase import FileSystemTestCase
from vimswitch.Settings import Settings
from mock import patch
from vimswitch.Application import Application
from vimswitch.VimSwitch import VimSwitch
from vimswitch.six import StringIO


class TestVimSwitch(FileSystemTestCase):

    def setUp(self):
        FileSystemTestCase.setUp(self)
        self.fakeInternetRoot = self.getDataPath('fake_internet')
        self.resetApplication()

    # Switch Profile

    def test_switchProfile_createsApplicationDirs(self):
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0)
        # Assert application dirs exist
        settings = self.app.settings
        self.assertDirExists(settings.configPath)
        self.assertDirExists(settings.cachePath)
        self.assertDirExists(settings.downloadsPath)

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_switchToRemoteProfile(self, stdout):
        self.copyDataToWorkingDir('home/.vimrc', '.vimrc')
        self.copyDataToWorkingDir('home/.vim', '.vim')
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0)
        # Assert default profile is created
        self.assertFileContents('.vimswitch/default/.vimrc', '" home vimrc data')
        self.assertDirExists('.vimswitch/default/.vim')
        # Assert home profile is replaced by downloaded profile
        self.assertFileContents('.vimrc', '" test vimrc data')
        self.assertDirExists('.vim')
        # Assert stdout
        self.assertStdout(stdout, """
            Saving profile: default
            Downloading profile from https://github.com/test/vimrc/archive/master.zip
            Switched to profile: test/vimrc
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_switchToNonExistantProfile_showsError(self, stdout):
        self.copyDataToWorkingDir('home/.vimrc', '.vimrc')
        self.copyDataToWorkingDir('home/.vim', '.vim')
        argv = ['./vimswitch', 'non_existant_profile']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, -1, stdout.getvalue())
        # Assert home profile is unchanged
        self.assertFileContents('.vimrc', '" home vimrc data')
        self.assertDirExists('.vim')
        # Assert stdout
        self.assertStdout(stdout, """
            Saving profile: default
            Downloading profile from https://github.com/non_existant_profile/archive/master.zip
            Error: .* 404 File not found
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_switchToAnotherProfile(self, stdout):
        argv1 = ['./vimswitch', 'test/vimrc']
        argv2 = ['./vimswitch', 'test2/vimrc']
        # Switch to an initial profile
        self.vimSwitch.main(argv1)
        self.resetApplication()
        self.resetStdout(stdout)

        # Now switch to another profile
        exitCode = self.vimSwitch.main(argv2)

        self.assertEqual(exitCode, 0, stdout.getvalue())
        # Assert current profile is now test2/vimrc
        self.assertFileContents('.vimrc', '" test2 vimrc data')
        self.assertDirExists('.vim')
        # Assert stdout
        self.assertStdout(stdout, """
            Saving profile: test/vimrc
            Downloading profile from https://github.com/test2/vimrc/archive/master.zip
            Switched to profile: test2/vimrc
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_switchToCachedProfile(self, stdout):
        argv1 = ['./vimswitch', 'test/vimrc']
        argv2 = ['./vimswitch', 'test2/vimrc']
        argv3 = ['./vimswitch', 'test/vimrc']
        # Download 2 profiles
        self.vimSwitch.main(argv1)
        self.resetApplication()
        self.vimSwitch.main(argv2)
        self.resetApplication()
        self.resetStdout(stdout)

        # Switch back to the first profile
        exitCode = self.vimSwitch.main(argv3)

        self.assertEqual(exitCode, 0, stdout.getvalue())
        # Assert current profile is now test/vimrc
        self.assertFileContents('.vimrc', '" test vimrc data')
        self.assertDirExists('.vim')
        # Assert stdout
        self.assertStdout(stdout, """
            Saving profile: test2/vimrc
            Switched to profile: test/vimrc
        """)

    def test_switchProfile_switchFromEmptyDefaultProfile(self):
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0)
        # Assert default profile is created and empty
        self.assertDirExists('.vimswitch/default')
        self.assertDirEmpty('.vimswitch/default')
        # Assert home profile is replaced by downloaded profile
        self.assertFileContents('.vimrc', '" test vimrc data')
        self.assertDirExists('.vim')

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
        self.assertPathDoesNotExist('.vimrc')
        self.assertPathDoesNotExist('.vim')

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
        self.assertFileContents('.vimswitch/default/.vimrc', '" home vimrc data')
        self.assertFileContents('.vimswitch/default/.vim/plugin/dummy_plugin.vim', '" dummy home vim plugin')
        self.assertDirExists('.vimswitch/default/.vim')
        # Assert home profile is replaced by downloaded profile
        self.assertFileContents('.vimrc', '" test vimrc data')
        self.assertDirExists('.vim')
        # Assert home profile no longer contains read-only file
        self.assertPathDoesNotExist('.vim/plugin/dummy_plugin.vim')
        # Assert stdout
        self.assertStdout(stdout, """
            Saving profile: default
            Downloading profile from https://github.com/test/vimrc/archive/master.zip
            Switched to profile: test/vimrc
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_switchProfile_savesChangesToCurrentProfile(self, stdout):
        self.copyDataToWorkingDir('home/.vimrc', '.vimrc')
        self.copyDataToWorkingDir('home/.vim', '.vim')
        argv1 = ['./vimswitch', 'test/vimrc']
        argv2 = ['./vimswitch', 'default']
        self.vimSwitch.main(argv1)
        self.resetApplication()
        self.resetStdout(stdout)
        homeVimrcFilePath = self.getTestPath('.vimrc')
        homeVimDirPath = self.getTestPath('.vim')
        diskIo = self.app.diskIo
        # Make changes to the test/vimrc profile
        diskIo.createFile(homeVimrcFilePath, '" updated vimrc data')
        diskIo.deleteDir(homeVimDirPath)

        self.vimSwitch.main(argv2)

        # Assert .vimrc changes saved
        self.assertFileContents('.vimswitch/test.vimrc/.vimrc', '" updated vimrc data')
        # Assert .vim dir deleted
        self.assertPathDoesNotExist('.vimswitch/test.vimrc/.vim')
        # Assert stdout
        self.assertStdout(stdout, """
            Saving profile: test/vimrc
            Switched to profile: default
        """)

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
            self.assertFileContents(filePath, 'test content')
        for dirPath in dirPaths:
            self.assertDirExists(dirPath)

    def test_switchProfile_switchFromWindowsProfile_movesWindowsProfileDataToCache(self):
        self.copyDataToWorkingDir('home/.vimrc', '_vimrc')
        self.copyDataToWorkingDir('home/.vim', '_vim')
        argv = ['./vimswitch', 'test/vimrc']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0)
        # Assert windows profile files are deleted
        self.assertPathDoesNotExist('_vimrc')
        self.assertPathDoesNotExist('_vim')
        # Assert windows profile moved to cache
        self.assertFileContents('.vimswitch/default/_vimrc', '" home vimrc data')
        self.assertDirExists('.vimswitch/default/_vim')
        # Assert home profile is replaced by downloaded profile
        self.assertFileContents('.vimrc', '" test vimrc data')
        self.assertDirExists('.vim')

    # Update profile

    @patch('sys.stdout', new_callable=StringIO)
    def test_updateProfile_redownloadsCachedProfile(self, stdout):
        self.runMain('./vimswitch test/vimrc')
        self.resetStdout(stdout)
        # Update profile on internet
        self.fakeInternetRoot = self.getDataPath('fake_internet2')

        # Now we update test/vimrc
        self.runMain('./vimswitch --update test/vimrc')

        self.assertEqual(self.exitCode, 0)
        self.assertFileContents('.vimrc', '" updated vimrc data')
        self.assertFileContents('.vimswitch/test.vimrc/.vimrc', '" updated vimrc data')
        self.assertDirExists('.vimswitch/test.vimrc/.vim')
        self.assertStdout(stdout, """
            Saving profile: test/vimrc
            Downloading profile from https://github.com/test/vimrc/archive/master.zip
            Switched to profile: test/vimrc
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_updateProfile_switchesToProfile(self, stdout):
        self.runMain('./vimswitch test/vimrc')
        self.runMain('./vimswitch test2/vimrc')
        self.resetStdout(stdout)
        # Update profile on internet
        self.fakeInternetRoot = self.getDataPath('fake_internet2')

        # Now we update test/vimrc
        self.runMain('./vimswitch --update test/vimrc')

        self.assertEqual(self.exitCode, 0)
        self.assertFileContents('.vimrc', '" updated vimrc data')
        self.assertFileContents('.vimswitch/test.vimrc/.vimrc', '" updated vimrc data')
        self.assertDirExists('.vimswitch/test.vimrc/.vim')
        self.assertStdout(stdout, """
            Saving profile: test2/vimrc
            Downloading profile from https://github.com/test/vimrc/archive/master.zip
            Switched to profile: test/vimrc
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_updateProfile_noArguments_updatesCurrentProfile(self, stdout):
        self.runMain('./vimswitch test/vimrc')
        self.resetStdout(stdout)
        # Update profile on internet
        self.fakeInternetRoot = self.getDataPath('fake_internet2')

        # Now we update test/vimrc
        self.runMain('./vimswitch --update')

        self.assertEqual(self.exitCode, 0)
        self.assertFileContents('.vimrc', '" updated vimrc data')
        self.assertFileContents('.vimswitch/test.vimrc/.vimrc', '" updated vimrc data')
        self.assertDirExists('.vimswitch/test.vimrc/.vim')
        self.assertStdout(stdout, """
            Saving profile: test/vimrc
            Downloading profile from https://github.com/test/vimrc/archive/master.zip
            Switched to profile: test/vimrc
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_updateProfile_downloadsUncachedProfile(self, stdout):
        self.runMain('./vimswitch --update test/vimrc')

        self.assertEqual(self.exitCode, 0)
        self.assertFileContents('.vimrc', '" test vimrc data')
        self.assertFileContents('.vimswitch/test.vimrc/.vimrc', '" test vimrc data')
        self.assertDirExists('.vimswitch/test.vimrc/.vim')
        self.assertStdout(stdout, """
            Saving profile: default
            Downloading profile from https://github.com/test/vimrc/archive/master.zip
            Switched to profile: test/vimrc
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_updateProfile_withDefaultProfile_showsError(self, stdout):
        self.runMain('./vimswitch test/vimrc')
        self.resetStdout(stdout)

        self.runMain('./vimswitch --update default')

        self.assertEqual(self.exitCode, -1)
        self.assertFileContents('.vimrc', '" test vimrc data')
        self.assertFileContents('.vimswitch/test.vimrc/.vimrc', '" test vimrc data')
        self.assertDirExists('.vimswitch/test.vimrc/.vim')
        self.assertStdout(stdout, """
            Cannot update default profile
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_updateProfile_withDefaultProfileAndNoArguments_showsError(self, stdout):
        self.runMain('./vimswitch --update')

        self.assertEqual(self.exitCode, -1)
        self.assertStdout(stdout, """
            Cannot update default profile
        """)

    # Show current profile

    @patch('sys.stdout', new_callable=StringIO)
    def test_noArguments_showsCurrentProfile(self, stdout):
        argv1 = ['./vimswitch', 'test/vimrc']
        argv2 = ['./vimswitch']
        self.vimSwitch.main(argv1)  # Sets current profile to test/vimrc
        self.resetApplication()
        self.resetStdout(stdout)

        exitCode = self.vimSwitch.main(argv2)

        self.assertEqual(exitCode, 0, stdout.getvalue())
        # Assert stdout
        self.assertStdout(stdout, """
            Current profile: test/vimrc
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_noArgumentsAndNoCurrentProfile_showsCurrentProfileIsNone(self, stdout):
        argv = ['./vimswitch']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, 0, stdout.getvalue())
        # Assert stdout
        self.assertStdout(stdout, """
            Current profile: None
        """)

    @patch('sys.stdout', new_callable=StringIO)
    def test_help(self, stdout):
        argvs = [
            ['./vimswitch', '-h'],
            ['./vimswitch', '--help']
        ]

        for argv in argvs:
            exitCode = self.vimSwitch.main(argv)

            self.assertEqual(exitCode, -1, stdout.getvalue())
            # Assert stdout
            helpRegex = """
                usage: vimswitch [-h] [-u] [profile]

                positional arguments:
                  profile

                optional arguments:
                  -h, --help    show this help message and exit
                  -u, --update
            """
            helpRegex = helpRegex.replace('[', r'\[')
            helpRegex = helpRegex.replace(']', r'\]')
            self.assertStdout(stdout, helpRegex)
            self.resetApplication()
            self.resetStdout(stdout)

    @patch('sys.stdout', new_callable=StringIO)
    def test_tooManyArgs_showsErrorMessage(self, stdout):
        argv = ['./vimswitch', 'test/vimrc', 'extra_argument']

        exitCode = self.vimSwitch.main(argv)

        self.assertEqual(exitCode, -1, stdout.getvalue())
        # Assert stdout
        self.assertStdout(stdout, """
            unrecognized arguments: extra_argument
            usage: vimswitch .*
            .*
        """)

    # Helpers

    def runMain(self, args):
        self.resetApplication()
        argv = args.split()
        self.exitCode = self.vimSwitch.main(argv)

    def resetApplication(self):
        """
        Resets the state of the application. This needs to be called every time
        before running vimswitch.main()
        """
        self.app = Application()
        self.app.settings = Settings(self.getWorkingDir())
        self.app.fileDownloader = createFakeFileDownloader(self.app, self.fakeInternetRoot)
        self.vimSwitch = VimSwitch(self.app)
        self.vimSwitch.raiseExceptions = True

    def createFile(self, path, contents):
        diskIo = self.app.diskIo
        path = self.getTestPath(path)
        diskIo.createFile(path, contents)

    def deleteDir(self, path):
        diskIo = self.app.diskIo
        path = self.getTestPath(path)
        diskIo.deleteDir(path)

    def assertFileContents(self, path, expectedContents):
        diskIo = self.app.diskIo
        path = self.getTestPath(path)
        actualContents = diskIo.getFileContents(path)
        self.assertEqual(actualContents, expectedContents)

    def assertDirExists(self, path):
        diskIo = self.app.diskIo
        path = self.getTestPath(path)
        self.assertTrue(diskIo.dirExists(path))

    def assertDirEmpty(self, path):
        diskIo = self.app.diskIo
        path = self.getTestPath(path)
        self.assertTrue(diskIo.isDirEmpty(path))

    def assertPathDoesNotExist(self, path):
        diskIo = self.app.diskIo
        path = self.getTestPath(path)
        self.assertFalse(diskIo.anyExists(path))
