import os
from mock import MagicMock
from vimswitch.Settings import Settings
from vimswitch.DiskIo import DiskIo
from vimswitch.ProfileDataIo import ProfileDataIo


# TODO: Inline this
def SettingsStub():
    settings = Settings(os.path.normpath('/home/foo'))
    return settings


def DiskIoStub():
    diskIo = MagicMock(DiskIo)
    return diskIo


def ProfileDataIoStub():
    profileDataIo = MagicMock(ProfileDataIo)
    return profileDataIo


# TODO: Inline this
def SettingsWorkingDirStub(workingDir):
    "Returns a Settings stub that treats `workingDir` as the home directory"
    settings = Settings(workingDir)
    return settings
