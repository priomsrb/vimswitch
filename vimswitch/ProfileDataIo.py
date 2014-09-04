class ProfileDataIo:
    def __init__(self, settings, diskIo):
        self.settings = settings
        self.diskIo = diskIo

    def delete(self, path):
        """Deletes profile data found at path"""
        for file in self.settings.getProfileFiles():
            # TODO: use python's path utils to make paths
            filePath = path + '/' + file
            if self.diskIo.fileExists(filePath):
                self.diskIo.deleteFile(filePath)

        for dir in self.settings.getProfileDirs():
            dirPath = path + '/' + dir
            if self.diskIo.dirExists(dirPath):
                self.diskIo.deleteDir(dirPath)

    def copy(self, srcPath, destPath):
        """
        Copies profile data from srcPath to destPath. Will replace existing
        files at destPath.
        """
        for file in self.settings.getProfileFiles():
            srcFilePath = srcPath + '/' + file
            destFilePath = destPath + '/' + file
            if self.diskIo.fileExists(srcFilePath):
                self.diskIo.copyFile(srcFilePath, destFilePath)

        for dir in self.settings.getProfileDirs():
            srcDirPath = srcPath + '/' + dir
            destDirPath = destPath + '/' + dir
            if self.diskIo.dirExists(srcDirPath):
                self.diskIo.copyDir(srcDirPath, destDirPath)
