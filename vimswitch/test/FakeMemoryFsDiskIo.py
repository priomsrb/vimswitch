from fs.memoryfs import MemoryFS
import fs.path
import os.path


class FakeMemoryFsDiskIo:
    "Uses fs.memoryfs to fake DiskIO"

    def __init__(self):
        self.fs = MemoryFS()

    def __del__(self):
        self.fs.close()

    def createFile(self, filePath, contents):
        filePath = fsPath(filePath)
        self.fs.setcontents(filePath, contents)

    def getFileContents(self, filePath):
        filePath = fsPath(filePath)
        return self.fs.getcontents(filePath).decode("utf-8")

    def copyFile(self, srcPath, destPath):
        srcPath = fsPath(srcPath)
        destPath = fsPath(destPath)

        # Convert destPath into a filename if it is a directory
        if self.dirExists(destPath):
            srcBasename = fs.path.basename(srcPath)
            destPath = fs.path.join(destPath, srcBasename)

        self.fs.copy(srcPath, destPath, overwrite=True)

    def move(self, srcPath, destPath):
        srcPath = fsPath(srcPath)
        destPath = fsPath(destPath)

        self.fs.move(srcPath, destPath, overwrite=True)

    def deleteFile(self, filePath):
        filePath = fsPath(filePath)
        self.fs.remove(filePath)

    def fileExists(self, filePath):
        filePath = fsPath(filePath)
        return self.fs.isfile(filePath)

    def createDir(self, dirPath):
        dirPath = fsPath(dirPath)
        self.fs.makedir(dirPath, recursive=False)

    def createDirWithParents(self, dirPath):
        dirPath = fsPath(dirPath)
        self.fs.makedir(dirPath, recursive=True)

    def copyDir(self, srcPath, destPath):
        srcPath = fsPath(srcPath)
        destPath = fsPath(destPath)

        # Create parent dirs if necessary
        destParentPath = fs.path.dirname(destPath)
        if not self.dirExists(destParentPath):
            self.createDirWithParents(destParentPath)

        self.fs.copydir(srcPath, destPath)

    def deleteDir(self, dirPath):
        dirPath = fsPath(dirPath)
        self.fs.removedir(dirPath, recursive=False, force=True)

    def dirExists(self, dirPath):
        dirPath = fsPath(dirPath)
        return self.fs.isdir(dirPath)

    def isDirEmpty(self, dirPath):
        dirPath = fsPath(dirPath)
        return self.fs.isdirempty(dirPath)

    def anyExists(self, path):
        path = fsPath(path)
        return self.fs.exists(path)


def fsPath(path):
    "Returns a path that is compatible with pyfilesystem"
    path = os.path.splitdrive(path)[1]
    path = path.replace('\\', '/')
    path = fs.path.normpath(path)
    return path
