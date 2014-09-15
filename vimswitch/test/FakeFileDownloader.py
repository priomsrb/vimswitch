import os
from vimswitch.DiskIo import createDiskIo


class FakeFileDownloader:
    """
    Fakes FileDownloader by downloading files from the filesystem. Download URLs
    are converted to a filesystem friendly format as follows:
        - `root` will be used as starting directory
        - Everything before the URL's basename will be used as the directory
          name
        - The filename will be the URL's basename
        - Replace '://' and '/' with '.'.

    For example, a call to
        `download('https://github.com/test/vimrc/archive/master.zip', path)`
    will copy the file located at
        `$root/https.github.com.test.vimrc.archive/master.zip` to `path`
    """

    def __init__(self, root, diskIo):
        self.root = os.path.normpath(root)
        self.diskIo = diskIo

    def download(self, url, path):
        (directory, baseName) = os.path.split(url)
        directory = directory.replace('://', '.').replace('/', '.')
        sourcePath = os.path.join(self.root, directory, baseName)
        if self.diskIo.dirExists(path):
            destPath = os.path.join(path, baseName)
        else:
            destPath = path

        self.diskIo.copyFile(sourcePath, destPath)
        return destPath


def createFakeFileDownloader(app, root):
    diskIo = app.get('diskIo', createDiskIo(app))
    fakeFileDownloader = FakeFileDownloader(root, diskIo)
    return fakeFileDownloader
