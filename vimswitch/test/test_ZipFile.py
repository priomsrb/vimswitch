from .FileSystemTestCase import FileSystemTestCase
from vimswitch.DiskIo import DiskIo
from zipfile import ZipFile


class TestZipFile(FileSystemTestCase):
    def setUp(self):
        FileSystemTestCase.setUp(self)
        self.diskIo = DiskIo()

    def test_extract_extractsFile(self):
        zipPath = self.getDataPath('simple.zip')
        destPath = self.getTestPath('')
        destFile1Path = self.getTestPath('file1.txt')
        destFile2Path = self.getTestPath('file2.txt')
        zipFile = ZipFile(zipPath)

        zipFile.extractall(destPath)

        file1Expected = 'test data'
        file1Actual = self.diskIo.getFileContents(destFile1Path)
        file2Expected = 'test data 2'
        file2Actual = self.diskIo.getFileContents(destFile2Path)
        self.assertTrue(file1Actual, file1Expected)
        self.assertTrue(file2Actual, file2Expected)
