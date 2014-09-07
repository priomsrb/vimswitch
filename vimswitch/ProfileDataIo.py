from Path import Path


class ProfileDataIo:
    def __init__(self, settings, diskIo):
        self.settings = settings
        self.diskIo = diskIo

    def delete(self, path):
        """Deletes profile data found at path"""
        for file in self.settings.getProfileFiles():
            filePath = path.join(file)
            if self.diskIo.fileExists(filePath):
                self.diskIo.deleteFile(filePath)

        for dir in self.settings.getProfileDirs():
            dirPath = path.join(dir)
            if self.diskIo.dirExists(dirPath):
                self.diskIo.deleteDir(dirPath)

    def copy(self, srcPath, destPath):
        """
        Copies profile data from srcPath to destPath. Will replace existing
        files at destPath.
        """
        for file in self.settings.getProfileFiles():
            srcFilePath = srcPath.join(file)
            destFilePath = destPath.join(file)
            if self.diskIo.fileExists(srcFilePath):
                self.diskIo.copyFile(srcFilePath, destFilePath)

        for dir in self.settings.getProfileDirs():
            srcDirPath = srcPath.join(dir)
            destDirPath = destPath.join(dir)
            if self.diskIo.dirExists(srcDirPath):
                self.diskIo.copyDir(srcDirPath, destDirPath)
