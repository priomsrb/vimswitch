from .test_DiskIo import TestDiskIo
from .FakeMemoryFsDiskIo import FakeMemoryFsDiskIo


class TestFakeMemoryFsDiskIo(TestDiskIo):
    def __init__(self, *args, **kwargs):
        TestDiskIo.__init__(self, *args, **kwargs)
        self.diskIoType = FakeMemoryFsDiskIo

    def setUp(self):
        TestDiskIo.setUp(self)
        if not self.diskIo.dirExists(self.getWorkingDir()):
            self.diskIo.createDirWithParents(self.getWorkingDir())
