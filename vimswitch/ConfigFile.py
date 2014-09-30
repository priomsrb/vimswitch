from .DiskIo import getDiskIo
from .Profile import Profile
from .six import StringIO
from .six.moves.configparser import SafeConfigParser


class ConfigFile:
    def __init__(self, diskIo):
        self.diskIo = diskIo

    def loadSettings(self, settings, path):
        """
        Reads the config file at path and applies the values to settings. If
        path does not exist, then settings will be left unchanged.
        """
        if self.diskIo.fileExists(path):
            settingsIo = StringIO(self.diskIo.getFileContents(path))
            config = self._getConfigParser()
            config.readfp(settingsIo)

            currentProfileName = config.get('settings', 'currentProfile')
            if currentProfileName is None:
                settings.currentProfile = None
            else:
                settings.currentProfile = Profile(currentProfileName)

    def saveSettings(self, settings, path):
        config = self._getConfigParser()
        config.add_section('settings')
        if settings.currentProfile is None:
            config.set('settings', 'currentProfile', None)
        else:
            config.set('settings', 'currentProfile', settings.currentProfile.name)

        settingsIo = StringIO()
        config.write(settingsIo)
        self.diskIo.createFile(path, settingsIo.getvalue())

    def _getConfigParser(self):
        # We set allow_no_value to True because settings.currentProfile can
        # sometimes be None
        configParser = SafeConfigParser(allow_no_value=True)
        return configParser


def getConfigFile(app):
    return app.get('configFile', createConfigFile(app))


def createConfigFile(app):
    diskIo = getDiskIo(app)
    configFile = ConfigFile(diskIo)
    return configFile
