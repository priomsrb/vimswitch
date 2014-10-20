from .DiskIo import getDiskIo
from zipfile import ZipFile
import os


class GithubZipballExtractor:
    def __init__(self, diskIo):
        self.diskIo = diskIo

    def extractZipball(self, zipFilename, path):
        '''
        Github zipballs contain a root folder with the repo contents inside.
        This method extracts the contents of that root folder into a path.

        For example a typical github zipball might look like:
            myrepo-master.zip/
                myrepo-master/
                    repo_file1
                    repo_file2
                    etc...

        This function will extract the repo contents directly into `path`:
            path/
                repo_file1
                repo_file2
                etc...
        '''
        ZipFile(zipFilename).extractall(path)
        rootDir = self._getRootDirName(zipFilename)
        rootDir = os.path.join(path, rootDir)
        self._moveDirContents(rootDir, path)
        self.diskIo.deleteDir(rootDir)

    def _moveDirContents(self, srcDir, destDir):
        dirContents = self.diskIo.getDirContents(srcDir)
        for item in dirContents:
            itemPath = os.path.join(srcDir, item)
            self.diskIo.move(itemPath, destDir)

    def _getRootDirName(self, zipFilename):
        zipContents = ZipFile(zipFilename).namelist()

        rootDirs = [dir for dir in zipContents if self._isZipRootDir(dir)]

        if len(rootDirs) > 1:
            raise IOError('Zipball %s has more than one root directory' % zipFilename)

        if len(rootDirs) < 1:
            raise IOError('Zipball %s has no root directory' % zipFilename)

        return rootDirs[0]

    def _isZipRootDir(self, path):
        if path.find('/') == len(path) - 1:
            return True
        else:
            return False


def getGithubZipballExtractor(app):
    return app.get('githubZipballExtractor', createGithubZipballExtractor(app))


def createGithubZipballExtractor(app):
    diskIo = getDiskIo(app)
    githubZipballExtractor = GithubZipballExtractor(diskIo)
    return githubZipballExtractor
