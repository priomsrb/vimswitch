import unittest
from .CommonDiskIoTests import CommonDiskIoTests
from .FakeFsDiskIo import FakeFsDiskIo


class TestFakeFsDiskIo(unittest.TestCase, CommonDiskIoTests):
    def setUp(self):
        self.diskIo = FakeFsDiskIo()
