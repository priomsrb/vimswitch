from .test_DiskIo import TestDiskIo
from .FakeFsDiskIo import FakeFsDiskIo


class TestFakeFsDiskIo(TestDiskIo):
    def __init__(self, *args, **kwargs):
        TestDiskIo.__init__(self, *args, **kwargs)
        self.diskIoType = FakeFsDiskIo

    def setUp(self):
        TestDiskIo.setUp(self)
        if not self.diskIo.dirExists(self.getWorkingDir()):
            self.diskIo.createDirWithParents(self.getWorkingDir())
