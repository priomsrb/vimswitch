from FileSystemTestCase import FileSystemTestCase
from vimswitch.DiskIo import DiskIo
from vimswitch.Profile import Profile
from vimswitch.ProfileCache import ProfileCache
from vimswitch.ProfileRetriever import ProfileRetriever
from Stubs import SettingsWorkingDirStub
from FakeFileDownloader import FakeFileDownloader


class TestProfileRetriever(FileSystemTestCase):
    def setUp(self):
        FileSystemTestCase.setUp(self)
        self.diskIo = DiskIo()

        self.settings = SettingsWorkingDirStub(self.getWorkingDir())
        self.diskIo.createDirWithParents(self.settings.downloadsPath)

        fileDownloader = FakeFileDownloader(self.getDataPath('fake_internet'), self.diskIo)

        profileCache = ProfileCache(self.settings, self.diskIo)

        self.profileRetriever = ProfileRetriever(self.settings, fileDownloader, profileCache, self.diskIo)

    def test_retrieve_retrievesProfile(self):
        profile = Profile('test/vimrc')

        self.profileRetriever.retrieve(profile)

        vimDirPath = self.getTestPath('.vimswitch/test.vimrc/.vim')
        vimrcFilePath = self.getTestPath('.vimswitch/test.vimrc/.vimrc')
        actualVimrcContent = self.diskIo.getFileContents(vimrcFilePath)
        expectedVimrcContent = '" test vimrc data'
        self.assertTrue(self.diskIo.dirExists(vimDirPath))
        self.assertEqual(actualVimrcContent, expectedVimrcContent)

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

    def test_retrieve_cannotDownloadProfile_raisesError(self):
        profile = Profile('non_existant/vimrc')

        self.assertRaises(IOError, self.profileRetriever.retrieve, profile)
