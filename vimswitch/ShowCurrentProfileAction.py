from .Action import Action
from .Settings import getSettings


class ShowCurrentProfileAction(Action):
    def __init__(self, settings):
        Action.__init__(self)
        self.settings = settings

    def execute(self):
        if self.settings.currentProfile is None:
            profileName = 'None'
        else:
            profileName = self.settings.currentProfile.name

        message = 'Current profile: %s' % profileName

        print(message.strip())


def createShowCurrentProfileAction(app):
    settings = getSettings(app)
    showCurrentProfileAction = ShowCurrentProfileAction(settings)
    return showCurrentProfileAction
