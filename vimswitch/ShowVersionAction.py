from .Action import Action
import platform
import vimswitch.version


class ShowVersionAction(Action):
    def __init__(self):
        Action.__init__(self)

    def execute(self):
        appVersion = vimswitch.version.__version__
        pythonVersion = platform.python_version()

        print("vimswitch %s (python %s)" % (appVersion, pythonVersion))


def createShowVersionAction(app):
    return ShowVersionAction()
