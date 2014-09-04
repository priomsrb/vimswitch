import shutil
import os


class DiskIo:

    def copyFile(self, srcPath, destPath):
        shutil.copy(srcPath, destPath)

    def deleteFile(self, filePath):
        os.remove(filePath)

    def fileExists(self, filePath):
        return os.path.isfile(filePath)

    def createDir(self, dirPath):
        return os.mkdir(dirPath)

    def copyDir(self, srcPath, destPath):
        """
        Recursively copies the src directory to a new dest directory. Creates
        the parent directories of the destination if required.

        Raises OSError if the destination directory already exists.
        """
        return shutil.copytree(srcPath, destPath)

    def deleteDir(self, dirPath):
        shutil.rmtree(dirPath)

    def dirExists(self, dirPath):
        return os.path.isdir(dirPath)
