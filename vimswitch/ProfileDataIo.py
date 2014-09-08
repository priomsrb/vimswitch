import os


class ProfileDataIo:
    def __init__(self, settings, diskIo):
        self.settings = settings
        self.diskIo = diskIo

    def delete(self, path):
        """Deletes profile data found at path"""
        for file in self.settings.profileFiles:
            filePath = os.path.join(path, file)
            if self.diskIo.fileExists(filePath):
                self.diskIo.deleteFile(filePath)

        for dir in self.settings.profileDirs:
            dirPath = os.path.join(path, dir)
            if self.diskIo.dirExists(dirPath):
                self.diskIo.deleteDir(dirPath)

    def copy(self, srcPath, destPath):
        """
        Copies profile data from srcPath to destPath. Will replace existing
        files at destPath.
        """
        for file in self.settings.profileFiles:
            srcFilePath = os.path.join(srcPath, file)
            destFilePath = os.path.join(destPath, file)
            if self.diskIo.fileExists(srcFilePath):
                self.diskIo.copyFile(srcFilePath, destFilePath)

        for dir in self.settings.profileDirs:
            srcDirPath = os.path.join(srcPath, dir)
            destDirPath = os.path.join(destPath, dir)
            if self.diskIo.dirExists(srcDirPath):
                self.diskIo.copyDir(srcDirPath, destDirPath)
