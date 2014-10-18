from .Action import Action
from .ProfileCache import getProfileCache
from .ProfileCopier import getProfileCopier
from .ProfileRetriever import getProfileRetriever
from .Settings import getSettings


class SwitchProfileAction(Action):

    def __init__(self, settings, profileCache, profileCopier, profileRetriever):
        Action.__init__(self)
        self.settings = settings
        self.profileCache = profileCache
        self.profileCopier = profileCopier
        self.profileRetriever = profileRetriever
        self.update = False
        self.profile = None

    def execute(self):
        self._saveCurrentProfile()
        self._retrieveProfile(self.profile)
        self.profileCopier.copyToHome(self.profile)
        self.settings.currentProfile = self.profile
        print('Switched to profile: %s' % self.profile.name)

    def _saveCurrentProfile(self):
        currentProfile = self._getCurrentProfile()
        print('Saving profile: %s' % currentProfile.name)
        self.profileCopier.copyFromHome(currentProfile)

    def _retrieveProfile(self, profile):
        if not self.profileCache.contains(profile) or self.update:
            self.profileRetriever.retrieve(profile)

    def _getCurrentProfile(self):
        if self.settings.currentProfile is None:
            currentProfile = self.settings.defaultProfile
        else:
            currentProfile = self.settings.currentProfile
        return currentProfile


def createSwitchProfileAction(app):
    settings = getSettings(app)
    profileCache = getProfileCache(app)
    profileCopier = getProfileCopier(app)
    profileRetriever = getProfileRetriever(app)
    switchProfileAction = SwitchProfileAction(settings, profileCache, profileCopier, profileRetriever)
    return switchProfileAction
