import os
from .Profile import Profile


class Settings:

    def __init__(self, homePath=''):
        """
        homePath is used as the prefix for all other paths. If homePath is not
        specified it gets set to the user's home directory.
        """
        self.homePath = homePath or os.path.expanduser('~')
        self.configPath = os.path.join(self.homePath, '.vimswitch')
        self.configFilePath = os.path.join(self.configPath, 'vimswitchrc')
        self.cachePath = os.path.join(self.configPath, 'profiles')
        self.downloadsPath = os.path.join(self.configPath, 'downloads')
        self.profileFiles = ['.vimrc', '_vimrc']
        self.profileDirs = ['.vim', '_vim']
        self.defaultProfile = Profile('default')
        self.currentProfile = None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def getSettings(app):
    return app.get('settings', createSettings(app))


def createSettings(app):
    return Settings()
