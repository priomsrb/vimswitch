from .BaseTestCase import BaseTestCase
from .CommonDiskIoTests import CommonDiskIoTests
from .FakeFsDiskIo import FakeFsDiskIo


class TestFakeFsDiskIo(BaseTestCase, CommonDiskIoTests):
    def setUp(self):
        self.diskIo = FakeFsDiskIo()
