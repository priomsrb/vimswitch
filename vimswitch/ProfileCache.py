import os


class ProfileCache:
    def __init__(self, settings, diskIo):
        self.settings = settings
        self.diskIo = diskIo

    def contains(self, profile):
        profileLocation = self.getLocation(profile)
        return self.diskIo.dirExists(profileLocation)

    def delete(self, profile):
        profileDirPath = self.getLocation(profile)
        self.diskIo.deleteDir(profileDirPath)

    def getLocation(self, profile):
        """Returns the path where profile is located"""
        fullPath = os.path.join(self.settings.cachePath, profile.getDirName())
        return os.path.normpath(fullPath)

    def createEmptyProfile(self, profile):
        location = self.getLocation(profile)
        self.diskIo.createDir(location)
