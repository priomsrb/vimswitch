import os


class ProfileCache:
    def __init__(self, settings, diskIo):
        self.settings = settings
        self.diskIo = diskIo

    def contains(self, profile):
        profileLocation = self.getLocation(profile)
        return self.diskIo.dirExists(profileLocation)

    def getLocation(self, profile):
        """Returns the path where profile is located"""
        fullPath = os.path.join(self.settings.getCacheDir(), profile.getDirName())
        return os.path.normpath(fullPath)

    def createEmptyProfile(self, profile):
        location = self.getLocation(profile)
        self.diskIo.createDir(location)
