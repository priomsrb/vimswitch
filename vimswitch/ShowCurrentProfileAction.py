from .Settings import getSettings


class ShowCurrentProfileAction():
    def __init__(self, settings):
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
