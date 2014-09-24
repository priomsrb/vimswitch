import unittest
from .CommonDiskIoTests import CommonDiskIoTests
from .FakeMemoryFsDiskIo import FakeMemoryFsDiskIo
from nose.plugins.attrib import attr


@attr('skip')
class TestFakeMemoryFsDiskIo(unittest.TestCase, CommonDiskIoTests):
    def setUp(self):
        self.diskIo = FakeMemoryFsDiskIo()
