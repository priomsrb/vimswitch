import unittest
from .CommonDiskIoTests import CommonDiskIoTests
from .FakeMemoryFsDiskIo import FakeMemoryFsDiskIo


class TestFakeMemoryFsDiskIo(unittest.TestCase, CommonDiskIoTests):
    def setUp(self):
        self.diskIo = FakeMemoryFsDiskIo()
