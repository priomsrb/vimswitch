from .FileSystemTestCase import FileSystemTestCase
from .CommonDiskIoTests import CommonDiskIoTests
from vimswitch.DiskIo import DiskIo


class TestDiskIo(FileSystemTestCase, CommonDiskIoTests):
    def setUp(self):
        self.diskIo = DiskIo()
        FileSystemTestCase.setUp(self)

    def getTestPath(self, path):
        return FileSystemTestCase.getTestPath(path)
