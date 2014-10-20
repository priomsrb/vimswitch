from .FakeFileDownloader import createFakeFileDownloader
from .FileSystemTestCase import FileSystemTestCase
from mock import patch
from vimswitch.Application import Application
from vimswitch.Profile import Profile
from vimswitch.ProfileRetriever import getProfileRetriever
from vimswitch.Settings import Settings
from vimswitch.six import StringIO


class TestProfileRetriever(FileSystemTestCase):
    def setUp(self):
        FileSystemTestCase.setUp(self)
        app = Application()

        app.settings = Settings(self.getWorkingDir())
        app.fileDownloader = createFakeFileDownloader(app, self.getDataPath('fake_internet'))

        self.profileRetriever = getProfileRetriever(app)
        self.diskIo = app.diskIo
        self.diskIo.createDirWithParents(app.settings.downloadsPath)

    def test_retrieve_retrievesProfile(self):
        profile = Profile('test/vimrc')

        self.profileRetriever.retrieve(profile)

        vimDirPath = self.getTestPath('.vimswitch/test.vimrc/.vim')
        vimrcFilePath = self.getTestPath('.vimswitch/test.vimrc/.vimrc')
        actualVimrcContent = self.diskIo.getFileContents(vimrcFilePath)
        expectedVimrcContent = '" test vimrc data'
        self.assertEqual(actualVimrcContent, expectedVimrcContent)
        self.assertTrue(self.diskIo.dirExists(vimDirPath))

    def test_retrieve_profileAlreadyCached_overwritesProfile(self):
        profile = Profile('test/vimrc')
        profileDirPath = self.getTestPath('.vimswitch/test.vimrc')
        vimDirPath = self.getTestPath('.vimswitch/test.vimrc/.vim')
        vimrcFilePath = self.getTestPath('.vimswitch/test.vimrc/.vimrc')
        self.diskIo.createDir(profileDirPath)
        self.diskIo.createDir(vimDirPath)
        self.diskIo.createFile(vimrcFilePath, '" previous data')

        self.profileRetriever.retrieve(profile)

        actualVimrcContent = self.diskIo.getFileContents(vimrcFilePath)
        expectedVimrcContent = '" test vimrc data'
        self.assertEqual(actualVimrcContent, expectedVimrcContent)
        self.assertTrue(self.diskIo.dirExists(vimDirPath))

    def test_retrieve_cannotDownloadProfile_raisesError(self):
        profile = Profile('non_existant/vimrc')

        self.assertRaises(IOError, self.profileRetriever.retrieve, profile)

    @patch('sys.stdout', new_callable=StringIO)
    def test_retrieve_prints(self, stdout):
        profile = Profile('test/vimrc')

        self.profileRetriever.retrieve(profile)

        self.assertStdout(stdout, 'Downloading profile from .*')
