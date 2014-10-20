from .FileSystemTestCase import FileSystemTestCase
from vimswitch.Application import Application
from vimswitch.GithubZipballExtractor import getGithubZipballExtractor


class TestGithubZipballExtractor(FileSystemTestCase):
    def setUp(self):
        FileSystemTestCase.setUp(self)
        app = Application()
        self.githubZipballExtractor = getGithubZipballExtractor(app)
        self.diskIo = app.diskIo

    def test_extract_extractsRepoFilesIntoPath(self):
        self.copyDataToWorkingDir('vimrc-master.zip', 'zipball.zip')
        zipballPath = self.getTestPath('zipball.zip')
        extractionDirPath = self.getTestPath('extractionDir')
        self.diskIo.createDir(extractionDirPath)

        self.githubZipballExtractor.extractZipball(zipballPath, extractionDirPath)

        self.assertFileContents('extractionDir/.vimrc', '" test vimrc data')
        self.assertDirExists('extractionDir/.vim')
        self.assertDirExists('extractionDir/.vim/plugin')
        self.assertFileContents('extractionDir/.vim/plugin/dummy_plugin.vim', '" dummy vim plugin')

    def test_extract_multipleRootDirs_raisesError(self):
        self.copyDataToWorkingDir('github_zipball_multiple_root_dirs.zip', 'zipball.zip')
        zipballPath = self.getTestPath('zipball.zip')
        extractionDirPath = self.getTestPath('extractionDir')
        self.diskIo.createDir(extractionDirPath)

        with self.assertRaises(IOError) as cm:
            self.githubZipballExtractor.extractZipball(zipballPath, extractionDirPath)

        self.assertRegexpMatches(str(cm.exception), 'Zipball .* has more than one root directory')

    def test_extract_noRootDir_raisesError(self):
        self.copyDataToWorkingDir('github_zipball_no_root_dir.zip', 'zipball.zip')
        zipballPath = self.getTestPath('zipball.zip')
        extractionDirPath = self.getTestPath('extractionDir')
        self.diskIo.createDir(extractionDirPath)

        with self.assertRaises(IOError) as cm:
            self.githubZipballExtractor.extractZipball(zipballPath, extractionDirPath)

        self.assertRegexpMatches(str(cm.exception), 'Zipball .* has no root directory')

    # Helpers

    def assertFileContents(self, path, expectedContents):
        diskIo = self.diskIo
        path = self.getTestPath(path)
        actualContents = diskIo.getFileContents(path)
        self.assertEqual(actualContents, expectedContents)

    def assertDirExists(self, path):
        diskIo = self.diskIo
        path = self.getTestPath(path)
        self.assertTrue(diskIo.dirExists(path))
