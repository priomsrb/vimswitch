import shutil
import os


class DiskIo:

    def createFile(self, filePath, contents):
        with open(filePath, 'w') as file:
            file.write(contents)

    def getFileContents(self, filePath):
        with open(filePath, 'r') as file:
            return file.read()

    def copyFile(self, srcPath, destPath):
        shutil.copy(srcPath, destPath)

    def move(self, srcPath, destPath):
        shutil.move(srcPath, destPath)

    def deleteFile(self, filePath):
        os.remove(filePath)

    def fileExists(self, filePath):
        return os.path.isfile(filePath)

    def createDir(self, dirPath):
        return os.mkdir(dirPath)

    def createDirWithParents(self, dirPath):
        return os.makedirs(dirPath)

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

    def anyExists(self, path):
        return self.fileExists(path) or self.dirExists(path)
