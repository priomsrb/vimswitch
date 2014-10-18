from .BaseTestCase import BaseTestCase
from .FileSystemSandbox import FileSystemSandbox
import os
import shutil
import stat


class FileSystemTestCase(BaseTestCase):
    """
    Inherit from this class when a unit test needs to access the disk. This
    class sets up a sandbox so that disk modifications only occur within a
    working directory. This keeps test code from affecting other files on the
    system.

    To get a path relative to  the working directory use getTestPath(). To get a
    path to test data use getDataPath().

    The working directory is cleared after every test so there is no need to do
    it manually within your tests.
    """

    def setUp(self):
        FileSystemSandbox.enable(self.getWorkingDir())
        self.clearWorkingDirectory()

    def tearDown(self):
        self.clearWorkingDirectory()
        FileSystemSandbox.disable()

    @classmethod
    def getMyDir(self):
        return os.path.dirname(__file__)

    @classmethod
    def getTestPath(self, path):
        "Returns path prepended by the working directory"
        fullPath = os.path.join(self.getWorkingDir(), path)
        return os.path.normpath(fullPath)

    @classmethod
    def getDataPath(self, path):
        "Returns path prepended by the test data directory"
        dataDir = 'data'
        fullPath = os.path.join(self.getMyDir(), dataDir, path)
        return os.path.normpath(fullPath)

    @classmethod
    def getWorkingDir(self):
        """"Returns the path to a directory where we can safely create files and
        directories during tests"""
        dirName = 'workingDir'
        return os.path.join(self.getMyDir(), dirName)

    def copyDataToWorkingDir(self, dataSrc, workingDirDest):
        "Copies a file or dir from the data directory to the working directory"
        dataSrc = self.getDataPath(dataSrc)
        workingDirDest = self.getTestPath(workingDirDest)
        if os.path.isdir(dataSrc):
            shutil.copytree(dataSrc, workingDirDest)
        else:
            shutil.copy(dataSrc, workingDirDest)

    def clearWorkingDirectory(self):
        for entry in os.listdir(self.getWorkingDir()):
            fullPath = os.path.join(self.getWorkingDir(), entry)
            if os.path.isfile(fullPath):
                # If file is readonly, make it writable
                if not os.access(fullPath, os.W_OK):
                    os.chmod(fullPath, stat.S_IWRITE)
                os.remove(fullPath)
            elif os.path.isdir(fullPath):
                shutil.rmtree(fullPath, onerror=_remove_readonly)


def _remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)
