import os
from mock import MagicMock
from vimswitch.Settings import Settings
from vimswitch.DiskIo import DiskIo
from vimswitch.ProfileDataIo import ProfileDataIo


def SettingsStub():
    settings = MagicMock(Settings)
    settings.profileFiles = ['.vimrc', '_vimrc']
    settings.profileDirs = ['.vim', '_vim']
    settings.homePath = os.path.normpath('/home/foo')
    settings.cachePath = os.path.normpath('/home/foo/.vimswitch')
    return settings


def DiskIoStub():
    diskIo = MagicMock(DiskIo)
    return diskIo


def ProfileDataIoStub():
    profileDataIo = MagicMock(ProfileDataIo)
    return profileDataIo
