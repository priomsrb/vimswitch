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


def SettingsWorkingDirStub(workingDir):
    "Returns a Settings stub that treats `workingDir` as the home directory"
    settings = Settings()
    settings.homePath = workingDir
    settings.configPath = os.path.join(settings.homePath, '.vimswitch')
    settings.cachePath = settings.configPath
    settings.downloadsPath = os.path.join(settings.cachePath, '.downloads')
    return settings
