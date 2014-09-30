from .BaseTestCase import BaseTestCase
from .CommonDiskIoTests import CommonDiskIoTests
from .FakeMemoryFsDiskIo import FakeMemoryFsDiskIo
from nose.plugins.attrib import attr


@attr('skip')
class TestFakeMemoryFsDiskIo(BaseTestCase, CommonDiskIoTests):
    def setUp(self):
        self.diskIo = FakeMemoryFsDiskIo()
