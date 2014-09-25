import shutil
import os
import stat


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
        """
        Recursively delete a directory. Read-only files inside the directory
        will also be deleted.
        """
        shutil.rmtree(dirPath, onerror=self._remove_readonly)

    def dirExists(self, dirPath):
        return os.path.isdir(dirPath)

    def isDirEmpty(self, dirPath):
        return len(os.listdir(dirPath)) == 0

    def anyExists(self, path):
        return self.fileExists(path) or self.dirExists(path)

    def setReadOnly(self, path, readOnly):
        if readOnly:
            os.chmod(path, stat.S_IREAD)
        else:
            os.chmod(path, stat.S_IWRITE)

    def isReadOnly(self, path):
        mode = os.stat(path)[stat.ST_MODE]
        return not mode & stat.S_IWRITE

    # Private

    def _remove_readonly(self, func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)


def getDiskIo(app):
    return app.get('diskIo', createDiskIo(app))


def createDiskIo(app):
    return DiskIo()
