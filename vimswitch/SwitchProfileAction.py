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
        self._saveCurrentProfile()
        self._retrieveProfile(profile)
        self.profileCopier.copyToHome(profile)
        self.settings.currentProfile = profile
        print('Switched to profile: %s' % profile.name)

    def _saveCurrentProfile(self):
        currentProfile = self._getCurrentProfile()
        print('Saving profile: %s' % currentProfile.name)
        self.profileCopier.copyFromHome(currentProfile)

    def _retrieveProfile(self, profile):
        if not self.profileCache.contains(profile):
            self.profileRetriever.retrieve(profile)

    def _getCurrentProfile(self):
        if self.settings.currentProfile is None:
            currentProfile = self.settings.defaultProfile
        else:
            currentProfile = self.settings.currentProfile
        return currentProfile


def getSwitchProfileAction(app):
    return app.get('switchProfileAction', createSwitchProfileAction(app))


def createSwitchProfileAction(app):
    settings = getSettings(app)
    profileCache = getProfileCache(app)
    profileCopier = getProfileCopier(app)
    profileRetriever = getProfileRetriever(app)
    switchProfileAction = SwitchProfileAction(settings, profileCache, profileCopier, profileRetriever)
    return switchProfileAction
