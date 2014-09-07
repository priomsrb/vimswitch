class ProfileCache:
    def __init__(self, settings, diskIo):
        self.settings = settings
        self.diskIo = diskIo

    def contains(self, profile):
        profileLocation = self.getLocation(profile)
        return self.diskIo.dirExists(profileLocation)

    def getLocation(self, profile):
        """Returns the path where profile is located"""
        return self.settings.getCacheDir().join(profile.getDirName())

    def createEmptyProfile(self, profile):
        location = self.getLocation(profile)
        self.diskIo.createDir(location)
