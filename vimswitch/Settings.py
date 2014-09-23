import os
from .Profile import Profile


class Settings:

    def __init__(self):
        self.defaultProfile = Profile('default')
        self.homePath = os.path.expanduser('~')
        self.configPath = os.path.join(self.homePath, '.vimswitch')
        self.cachePath = self.configPath
        self.downloadsPath = os.path.join(self.cachePath, '.downloads')
        self.profileFiles = ['.vimrc', '_vimrc']
        self.profileDirs = ['.vim', '_vim']


def getSettings(app):
    return app.get('settings', createSettings(app))


def createSettings(app):
    return Settings()
