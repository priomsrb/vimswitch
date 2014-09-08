import os


class Settings:

    def __init__(self):
        self.defaultProfile = 'default'
        self.homePath = os.path.expanduser('~')
        self.cachePath = os.path.join(self.homePath, '.vimswitch')
        self.profileFiles = ['.vimrc', '_vimrc']
        self.profileDirs = ['.vim', '_vim']
