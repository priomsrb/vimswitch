import fake_filesystem
import fake_filesystem_shutil


class FakeFsDiskIo:
    "Uses pyfakefs to fake DiskIo operations"

    def __init__(self):
        self.fs = fake_filesystem.FakeFilesystem()
        self.fake_os = fake_filesystem.FakeOsModule(self.fs)
        self.fake_shutil = fake_filesystem_shutil.FakeShutilModule(self.fs)
        self.fake_open = fake_filesystem.FakeFileOpen(self.fs)

    def createFile(self, filePath, contents):
        with self.fake_open(filePath, 'w') as file:
            file.write(contents)

    def getFileContents(self, filePath):
        with self.fake_open(filePath, 'r') as file:
            return file.read()

    def copyFile(self, srcPath, destPath):
        self.fake_shutil.copy(srcPath, destPath)

    def move(self, srcPath, destPath):
        self.fake_shutil.move(srcPath, destPath)

    def deleteFile(self, filePath):
        self.fake_os.remove(filePath)

    def fileExists(self, filePath):
        return self.fake_os.path.isfile(filePath)

    def createDir(self, dirPath):
        return self.fake_os.mkdir(dirPath)

    def createDirWithParents(self, dirPath):
        return self.fake_os.makedirs(dirPath)

    def copyDir(self, srcPath, destPath):
        """
        Recursively copies the src directory to a new dest directory. Creates
        the parent directories of the destination if required.

        Raises OSError if the destination directory already exists.
        """
        return self.fake_shutil.copytree(srcPath, destPath)

    def deleteDir(self, dirPath):
        self.fake_shutil.rmtree(dirPath)

    def dirExists(self, dirPath):
        return self.fake_os.path.isdir(dirPath)

    def isDirEmpty(self, dirPath):
        return len(self.fake_os.listdir(dirPath)) == 0

    def anyExists(self, path):
        return self.fileExists(path) or self.dirExists(path)
