from .FileSystemTestCase import FileSystemTestCase
from .SimpleServer import SimpleServer
from vimswitch.DiskIo import DiskIo
from vimswitch.FileDownloader import FileDownloader
from vimswitch.Settings import Settings
from mock import MagicMock
from nose.plugins.attrib import attr
from email.message import Message


@attr('slow')
class TestFileDownloader(FileSystemTestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8001
        cls.host = 'localhost'
        cls.server = SimpleServer(cls.getDataPath(''), cls.host, cls.port)
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        FileSystemTestCase.setUp(self)
        settings = Settings()
        settings.downloadsPath = self.getTestPath('')
        self.diskIo = DiskIo()
        self.fileDownloader = FileDownloader(settings, self.diskIo)

    # FileDownloader.download

    def test_download_downloadsFile(self):
        url = self.getLocalUrl('simple.txt')
        downloadPath = self.getTestPath('simple_downloaded.txt')

        self.fileDownloader.download(url, downloadPath)

        actual = self.diskIo.getFileContents(downloadPath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    @attr('external')
    def test_download_downloadsFromHttps(self):
        url = 'https://github.com/priomsrb/vimrc/archive/master.zip'
        downloadDir = self.getTestPath('')

        downloadPath = self.fileDownloader.download(url, downloadDir)

        self.assertTrue(self.diskIo.fileExists(downloadPath))

    def test_download_fileAlreadyExists_overwritesFile(self):
        url = self.getLocalUrl('simple.txt')
        downloadPath = self.getTestPath('simple_downloaded.txt')
        self.diskIo.createFile(downloadPath, 'previous data')

        self.fileDownloader.download(url, downloadPath)

        actual = self.diskIo.getFileContents(downloadPath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_download_nonExistantUrl_raisesError(self):
        nonExistantUrl = self.getLocalUrl('non_existant.txt')
        downloadDir = self.getTestPath('')

        self.assertRaises(IOError, self.fileDownloader.download, nonExistantUrl, downloadDir)

    def test_download_dirAsDestination_keepsOriginalFilename(self):
        url = self.getLocalUrl('simple.txt')
        downloadDir = self.getTestPath('')

        downloadPath = self.fileDownloader.download(url, downloadDir)

        self.assertEqual(downloadPath, self.getTestPath('simple.txt'))
        actual = self.diskIo.getFileContents(downloadPath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_download_withMissingFilename_generatesFilename(self):
        url = self.getLocalUrl('simple.txt')
        downloadDir = self.getTestPath('')
        self.fileDownloader._getDownloadFilename = MagicMock(FileDownloader._getDownloadFilename)
        self.fileDownloader._getDownloadFilename.return_value = ''

        downloadPath = self.fileDownloader.download(url, downloadDir)

        self.assertTrue(len(downloadPath) > 0)
        actual = self.diskIo.getFileContents(downloadPath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    # FileDownloader._getDownloadFilename

    def test_getDownloadFilename_parsesUrl(self):
        url = 'http://example.com/foo/bar/file.txt?q=1'
        headers = Message()
        filename = self.fileDownloader._getDownloadFilename(url, headers)
        self.assertEqual(filename, 'file.txt')

    def test_getDownloadFilename_parsesHeader(self):
        url = ''
        headers = Message()
        headers['Server'] = 'SimpleHTTP/0.6 Python/2.7.5'
        headers['Date'] = 'Tue, 09 Sep 2014 02:51:53 GMT'
        headers['Content-type'] = 'text/plain'
        headers['Content-Length'] = '9'
        headers['Last-Modified'] = 'Mon, 08 Sep 2014 23:53:51 GMT'
        # content-disposition should specify the filename
        headers['content-disposition'] = 'attachment; filename=file.txt'
        filename = self.fileDownloader._getDownloadFilename(url, headers)
        self.assertEqual(filename, 'file.txt')

    # Helpers

    def getLocalUrl(self, path):
        return 'http://' + self.host + ':' + str(self.port) + '/' + path
