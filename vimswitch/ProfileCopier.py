class ProfileCopier:
    def __init__(self, settings, profileCache, profileDataIo):
        self.settings = settings
        self.profileCache = profileCache
        self.profileDataIo = profileDataIo

    def copyToHome(self, profile):
        """
        Copies the cached profile to home, thus making it active
        """
        # TODO: If profileDataIo.copy fails, then we are left with an empty
        # profile at home. So we should use the 'operate on temp then rename'
        # pattern
        homePath = self.settings.homePath
        profilePath = self.profileCache.getLocation(profile)
        self.profileDataIo.delete(homePath)
        self.profileDataIo.copy(profilePath, homePath)

    def copyFromHome(self, profile):
        """
        Copies the active profile data at home to a specified profile in cache
        (usually 'default')
        """
        if not self.profileCache.contains(profile):
            self.profileCache.createEmptyProfile(profile)
        profilePath = self.profileCache.getLocation(profile)
        homePath = self.settings.homePath
        self.profileDataIo.delete(profilePath)
        self.profileDataIo.copy(homePath, profilePath)
