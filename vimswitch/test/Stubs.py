import os
from mock import MagicMock
from vimswitch.Settings import Settings
from vimswitch.DiskIo import DiskIo
from vimswitch.ProfileDataIo import ProfileDataIo


def SettingsStub():
    settings = MagicMock(Settings)
    settings.getProfileFiles.return_value = ['.vimrc', '_vimrc']
    settings.getProfileDirs.return_value = ['.vim', '_vim']
    settings.getHomeDir.return_value = os.path.normpath('/home/foo')
    settings.getCacheDir.return_value = os.path.normpath('/home/foo/.vimswitch')
    return settings


def DiskIoStub():
    diskIo = MagicMock(DiskIo)
    return diskIo


def ProfileDataIoStub():
    profileDataIo = MagicMock(ProfileDataIo)
    return profileDataIo
