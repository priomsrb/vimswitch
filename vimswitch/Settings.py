import os


class Settings:

    def __init__(self):
        self.defaultProfile = 'default'
        self.homePath = os.path.expanduser('~')
        self.configPath = os.path.join(self.homePath, '.vimswitch')
        self.cachePath = self.configPath
        self.downloadsPath = os.path.join(self.cachePath, '.downloads')
        self.profileFiles = ['.vimrc', '_vimrc']
        self.profileDirs = ['.vim', '_vim']
