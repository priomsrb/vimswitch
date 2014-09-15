import unittest
import os
import shutil
import __builtin__


class FileSystemTestCase(unittest.TestCase):
    def setUp(self):
        self.setUpSafeOperations()
        self.clearWorkingDirectory()

    def tearDown(self):
        self.clearWorkingDirectory()
        self.tearDownSafeOperations()

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

    def clearWorkingDirectory(self):
        for entry in os.listdir(self.getWorkingDir()):
            fullPath = os.path.join(self.getWorkingDir(), entry)
            if os.path.isfile(fullPath):
                os.remove(fullPath)
            elif os.path.isdir(fullPath):
                shutil.rmtree(fullPath)

    def setUpSafeOperations(self):
        self.real_builtin_open = __builtin__.open
        self.real_os_mkdir = os.mkdir
        self.real_os_makedirs = os.makedirs
        self.real_os_remove = os.remove
        self.real_os_path_isfile = os.path.isfile
        self.real_os_path_isdir = os.path.isdir
        self.real_shutil_copy = shutil.copy
        self.real_shutil_move = shutil.move
        self.real_shutil_copytree = shutil.copytree
        self.real_shutil_rmtree = shutil.rmtree

        __builtin__.open = self.safe_builtin_open
        os.mkdir = self.safe_os_mkdir
        os.makedirs = self.safe_os_makedirs
        os.remove = self.safe_os_remove
        shutil.copy = self.safe_shutil_copy
        shutil.move = self.safe_shutil_move
        shutil.copytree = self.safe_shutil_copytree
        shutil.rmtree = self.safe_shutil_rmtree

    def tearDownSafeOperations(self):
        __builtin__.open = self.real_builtin_open
        os.mkdir = self.real_os_mkdir
        os.makedirs = self.real_os_makedirs
        os.remove = self.real_os_remove
        shutil.copy = self.real_shutil_copy
        shutil.move = self.real_shutil_move
        shutil.copytree = self.real_shutil_copytree
        shutil.rmtree = self.real_shutil_rmtree

    def safe_builtin_open(self, path, mode='r', buffering=-1):
        # We only verify if the file is being opened for writing or appending
        # This is because the unit test framework itself tries to read files
        # outside the working directory when a test fails
        if mode.find('w') != -1 or mode.find('a') != -1:
            self.verifyPath(path)
        return self.real_builtin_open(path, mode, buffering)

    def safe_os_mkdir(self, path, mode=0777):
        self.verifyPath(path)
        self.real_os_mkdir(path, mode)

    def safe_os_makedirs(self, path, mode=0777):
        self.verifyPath(path)
        self.real_os_makedirs(path, mode)

    def safe_os_remove(self, path):
        self.verifyPath(path)
        self.real_os_remove(path)

    def safe_shutil_copy(self, src, dst):
        # Only need to verify destination path since src will not be modified
        self.verifyPath(dst)
        self.real_shutil_copy(src, dst)

    def safe_shutil_move(self, src, dst):
        self.verifyPath(src)
        self.verifyPath(dst)
        self.real_shutil_move(src, dst)

    def safe_shutil_copytree(self, src, dst, symlinks=False, ignore=None):
        self.verifyPath(src)
        self.verifyPath(dst)
        self.real_shutil_copytree(src, dst, symlinks, ignore)

    def safe_shutil_rmtree(self, path, ignore_errors=False, onerror=None):
        self.verifyPath(path)
        self.real_shutil_rmtree(path, ignore_errors, onerror)

    def verifyPath(self, path):
        "Checks that path is inside the working directory"
        absPath = os.path.abspath(path)
        if not absPath.startswith(self.getWorkingDir()):
            raise TestSandboxError(path)


class TestSandboxError(Exception):
    def __init__(self, path):
        Exception.__init__(self, 'Tried to access path outside test working directory: %s' % path)
