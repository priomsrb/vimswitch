from .FileSystemTestCase import FileSystemTestCase
from vimswitch.Settings import Settings
from vimswitch.DiskIo import getDiskIo
from vimswitch.ApplicationDirs import getApplicationDirs
from vimswitch.Application import Application


class TestApplicationDirs(FileSystemTestCase):
    def setUp(self):
        FileSystemTestCase.setUp(self)
        app = Application()
        app.settings = Settings(self.getWorkingDir())
        self.settings = app.settings
        self.diskIo = getDiskIo(app)
        self.applicationDirs = getApplicationDirs(app)

    def test_createIfNone_noApplicationDirs_createsApplicationDirs(self):
        self.applicationDirs.createIfNone()

        dirExists = self.diskIo.dirExists
        self.assertTrue(dirExists(self.settings.configPath))
        self.assertTrue(dirExists(self.settings.cachePath))
        self.assertTrue(dirExists(self.settings.downloadsPath))

    def test_createIfNone_applicationDirsExist_doesNothing(self):
        # Create dirs
        self.applicationDirs.createIfNone()

        # Application Dirs now exist. Create again
        self.applicationDirs.createIfNone()

        # No Exceptions should be raised
