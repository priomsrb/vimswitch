import unittest
import os
import shutil


class IntegrationTestCase(unittest.TestCase):
    def getMyDir(self):
        return os.path.dirname(__file__)

    def getFullPath(self, path):
        return os.path.join(self.getWorkingDir(), path)

    def getWorkingDir(self):
        dirName = 'workingDir'
        return os.path.join(self.getMyDir(), dirName)

    def clearWorkingDirectory(self):
        for entry in os.listdir(self.getWorkingDir()):
            fullPath = os.path.join(self.getWorkingDir(), entry)
            if os.path.isfile(fullPath):
                os.remove(fullPath)
            elif os.path.isdir(fullPath):
                shutil.rmtree(fullPath)
