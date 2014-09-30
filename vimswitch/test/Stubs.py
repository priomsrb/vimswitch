from mock import MagicMock
from vimswitch.DiskIo import DiskIo
from vimswitch.ProfileDataIo import ProfileDataIo


def DiskIoStub():
    diskIo = MagicMock(DiskIo)
    return diskIo


def ProfileDataIoStub():
    profileDataIo = MagicMock(ProfileDataIo)
    return profileDataIo
