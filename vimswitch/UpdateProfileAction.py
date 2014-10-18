from .Settings import getSettings
from .SwitchProfileAction import createSwitchProfileAction


class UpdateProfileAction:
    def __init__(self, settings, switchProfileAction):
        self.settings = settings
        self.switchProfileAction = switchProfileAction
        self.profile = None
        self.exitCode = 0

    def execute(self):
        self.profile = self._getProfile()

        if self.profile == self.settings.defaultProfile:
            print('Cannot update default profile')
            self.exitCode = -1
            return

        self.switchProfileAction.update = True
        self.switchProfileAction.switchToProfile(self.profile)

    def _getProfile(self):
        if self.profile is None:
            if self.settings.currentProfile is None:
                return self.settings.defaultProfile
            else:
                return self.settings.currentProfile
        else:
            return self.profile


def createUpdateProfileAction(app):
    settings = getSettings(app)
    switchProfileAction = createSwitchProfileAction(app)
    updateProfileAction = UpdateProfileAction(settings, switchProfileAction)
    return updateProfileAction
