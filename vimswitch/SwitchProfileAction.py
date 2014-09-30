from .Settings import getSettings
from .ProfileCache import getProfileCache
from .ProfileCopier import getProfileCopier
from .ProfileRetriever import getProfileRetriever


class SwitchProfileAction:

    def __init__(self, settings, profileCache, profileCopier, profileRetriever):
        self.settings = settings
        self.profileCache = profileCache
        self.profileCopier = profileCopier
        self.profileRetriever = profileRetriever

    def switchToProfile(self, profile):
        self._createDefaultProfile()
        self._retrieveProfile(profile)
        self.profileCopier.copyToHome(profile)
        self.settings.currentProfile = profile
        print('Switched to profile: %s' % profile.name)

    def _createDefaultProfile(self):
        defaultProfile = self.settings.defaultProfile
        if not self.profileCache.contains(defaultProfile):
            self.profileCopier.copyFromHome(defaultProfile)

    def _retrieveProfile(self, profile):
        if not self.profileCache.contains(profile):
            self.profileRetriever.retrieve(profile)


def getSwitchProfileAction(app):
    return app.get('switchProfileAction', createSwitchProfileAction(app))


def createSwitchProfileAction(app):
    settings = getSettings(app)
    profileCache = getProfileCache(app)
    profileCopier = getProfileCopier(app)
    profileRetriever = getProfileRetriever(app)
    switchProfileAction = SwitchProfileAction(settings, profileCache, profileCopier, profileRetriever)
    return switchProfileAction
