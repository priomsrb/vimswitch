from .DiskIo import getDiskIo
from .Settings import getSettings


class ApplicationDirs:
    def __init__(self, settings, diskIo):
        self.settings = settings
        self.diskIo = diskIo

    def createIfNone(self):
        self._createDir(self.settings.configPath)
        self._createDir(self.settings.cachePath)
        self._createDir(self.settings.downloadsPath)

    def _createDir(self, path):
        if not self.diskIo.dirExists(path):
            self.diskIo.createDir(path)


def getApplicationDirs(app):
    return app.get('applicationDirs', createApplicationDirs(app))


def createApplicationDirs(app):
    settings = getSettings(app)
    diskIo = getDiskIo(app)
    applicationDirs = ApplicationDirs(settings, diskIo)
    return applicationDirs
