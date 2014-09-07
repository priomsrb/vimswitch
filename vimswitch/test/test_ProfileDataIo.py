import unittest
import Stubs
from TestHelpers import assertNoCall
from vimswitch.Path import Path
from vimswitch.ProfileDataIo import ProfileDataIo


class TestProfileDataIo(unittest.TestCase):
    def setUp(self):
        self.diskIo = Stubs.DiskIoStub()
        self.settings = Stubs.SettingsStub()
        self.profileDataIo = ProfileDataIo(self.settings, self.diskIo)

    # ProfileDataIo.delete#files

    def test_delete_whenFileExists_deletesFile(self):
        profilePath = Path('/home/foo')
        self.diskIo.fileExists.return_value = True

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteFile.assert_any_call(Path('/home/foo/.vimrc'))

    def test_delete_whenFileDoesNotExists_doesNotDeleteFile(self):
        profilePath = Path('/home/foo')
        self.diskIo.fileExists.return_value = False

        self.profileDataIo.delete(profilePath)

        assertNoCall(self.diskIo.deleteFile, Path('/home/foo/.vimrc'))

    def test_delete_usesGetProfileFiles_fromSettings(self):
        profilePath = Path('/home/foo')
        self.diskIo.fileExists.return_value = True
        self.settings.getProfileFiles.return_value = ['testProfileFile']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteFile.assert_any_call(Path('/home/foo/testProfileFile'))

    def test_delete_deletesMultipleFiles(self):
        profilePath = Path('/home/foo')
        self.diskIo.fileExists.return_value = True
        self.settings.getProfileFiles.return_value = ['file1', 'file2']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteFile.assert_any_call(Path('/home/foo/file1'))
        self.diskIo.deleteFile.assert_any_call(Path('/home/foo/file2'))

    # ProfileDataIo.delete#dirs

    def test_delete_whenDirExists_deletesDir(self):
        profilePath = Path('/home/foo')
        self.diskIo.dirExists.return_value = True

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteDir.assert_any_call(Path('/home/foo/.vim'))

    def test_delete_whenDirDoesNotExists_doesNotDeleteDir(self):
        profilePath = Path('/home/foo')
        self.diskIo.dirExists.return_value = False

        self.profileDataIo.delete(profilePath)

        assertNoCall(self.diskIo.deleteDir, Path('/home/foo/.vim'))

    def test_delete_usesGetProfileDirs_fromSettings(self):
        profilePath = Path('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.getProfileDirs.return_value = ['testProfileDir']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteDir.assert_any_call(Path('/home/foo/testProfileDir'))

    def test_delete_deletesMultipleDirs(self):
        profilePath = Path('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.getProfileDirs.return_value = ['dir1', 'dir2']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteDir.assert_any_call(Path('/home/foo/dir1'))
        self.diskIo.deleteDir.assert_any_call(Path('/home/foo/dir2'))

    def test_delete_deletesFilesAndDirs(self):
        profilePath = Path('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.getProfileFiles.return_value = ['file1', 'file2']
        self.settings.getProfileDirs.return_value = ['dir1', 'dir2']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteFile.assert_any_call(Path('/home/foo/file1'))
        self.diskIo.deleteFile.assert_any_call(Path('/home/foo/file2'))
        self.diskIo.deleteDir.assert_any_call(Path('/home/foo/dir1'))
        self.diskIo.deleteDir.assert_any_call(Path('/home/foo/dir2'))

    # ProfileDataIo.copy#files

    def test_copy_whenFileExists_copiesFile(self):
        srcPath = Path('/home/foo/.vimswitch/test.vimrc')
        destPath = Path('/home/foo')
        self.diskIo.fileExists.return_value = True

        self.profileDataIo.copy(srcPath, destPath)

        srcFile = Path('/home/foo/.vimswitch/test.vimrc/.vimrc')
        destFile = Path('/home/foo/.vimrc')
        self.diskIo.copyFile.assert_any_call(srcFile, destFile)

    def test_copy_whenFileDoesNotExists_doesNotCopyFile(self):
        srcPath = Path('/home/foo/.vimswitch/test.vimrc')
        destPath = Path('/home/foo')
        self.diskIo.fileExists.return_value = False

        self.profileDataIo.copy(srcPath, destPath)

        srcFile = Path('/home/foo/.vimswitch/test.vimrc/.vimrc')
        destFile = Path('/home/foo/.vimrc')
        assertNoCall(self.diskIo.copyFile, srcFile, destFile)

    def test_copy_usesGetProfileFiles_fromSettings(self):
        srcPath = Path('/home/foo/.vimswitch/test.vimrc')
        destPath = Path('/home/foo')
        self.diskIo.fileExists.return_value = True
        self.settings.getProfileFiles.return_value = ['testProfileFile']

        self.profileDataIo.copy(srcPath, destPath)

        srcFile = Path('/home/foo/.vimswitch/test.vimrc/testProfileFile')
        destFile = Path('/home/foo/testProfileFile')
        self.diskIo.copyFile.assert_any_call(srcFile, destFile)

    def test_copy_copiesMultipleFiles(self):
        srcPath = Path('/home/foo/.vimswitch/test.vimrc')
        destPath = Path('/home/foo')
        self.diskIo.fileExists.return_value = True
        self.settings.getProfileFiles.return_value = ['file1', 'file2']

        self.profileDataIo.copy(srcPath, destPath)

        srcFile1 = Path('/home/foo/.vimswitch/test.vimrc/file1')
        destFile1 = Path('/home/foo/file1')
        srcFile2 = Path('/home/foo/.vimswitch/test.vimrc/file2')
        destFile2 = Path('/home/foo/file2')
        self.diskIo.copyFile.assert_any_call(srcFile1, destFile1)
        self.diskIo.copyFile.assert_any_call(srcFile2, destFile2)

    # ProfileDataIo.copy#dirs

    def test_copy_whenDirExists_copiesDir(self):
        srcPath = Path('/home/foo/.vimswitch/test.vimrc')
        destPath = Path('/home/foo')
        self.diskIo.dirExists.return_value = True

        self.profileDataIo.copy(srcPath, destPath)

        srcDir = Path('/home/foo/.vimswitch/test.vimrc/.vim')
        destDir = Path('/home/foo/.vim')
        self.diskIo.copyDir.assert_any_call(srcDir, destDir)

    def test_copy_whenDirDoesNotExists_doesNotCopyDir(self):
        srcPath = Path('/home/foo/.vimswitch/test.vimrc')
        destPath = Path('/home/foo')
        self.diskIo.dirExists.return_value = False

        self.profileDataIo.copy(srcPath, destPath)

        srcDir = Path('/home/foo/.vimswitch/test.vimrc/.vim')
        destDir = Path('/home/foo/.vim')
        assertNoCall(self.diskIo.copyDir, srcDir, destDir)

    def test_copy_usesGetProfileDirs_fromSettings(self):
        srcPath = Path('/home/foo/.vimswitch/test.vimrc')
        destPath = Path('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.getProfileDirs.return_value = ['testProfileDir']

        self.profileDataIo.copy(srcPath, destPath)

        srcDir = Path('/home/foo/.vimswitch/test.vimrc/testProfileDir')
        destDir = Path('/home/foo/testProfileDir')
        self.diskIo.copyDir.assert_any_call(srcDir, destDir)

    def test_copy_copiesMultipleDirs(self):
        srcPath = Path('/home/foo/.vimswitch/test.vimrc')
        destPath = Path('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.getProfileDirs.return_value = ['dir1', 'dir2']

        self.profileDataIo.copy(srcPath, destPath)

        srcDir1 = Path('/home/foo/.vimswitch/test.vimrc/dir1')
        destDir1 = Path('/home/foo/dir1')
        srcDir2 = Path('/home/foo/.vimswitch/test.vimrc/dir2')
        destDir2 = Path('/home/foo/dir2')
        self.diskIo.copyDir.assert_any_call(srcDir1, destDir1)
        self.diskIo.copyDir.assert_any_call(srcDir2, destDir2)

    def test_copy_copiesFilesAndDirs(self):
        srcPath = Path('/home/foo/.vimswitch/test.vimrc')
        destPath = Path('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.getProfileFiles.return_value = ['file1', 'file2']
        self.settings.getProfileDirs.return_value = ['dir1', 'dir2']

        self.profileDataIo.copy(srcPath, destPath)

        srcFile1 = Path('/home/foo/.vimswitch/test.vimrc/file1')
        destFile1 = Path('/home/foo/file1')
        srcFile2 = Path('/home/foo/.vimswitch/test.vimrc/file2')
        destFile2 = Path('/home/foo/file2')
        srcDir1 = Path('/home/foo/.vimswitch/test.vimrc/dir1')
        destDir1 = Path('/home/foo/dir1')
        srcDir2 = Path('/home/foo/.vimswitch/test.vimrc/dir2')
        destDir2 = Path('/home/foo/dir2')
        self.diskIo.copyFile.assert_any_call(srcFile1, destFile1)
        self.diskIo.copyFile.assert_any_call(srcFile2, destFile2)
        self.diskIo.copyDir.assert_any_call(srcDir1, destDir1)
        self.diskIo.copyDir.assert_any_call(srcDir2, destDir2)

    # TODO: Add tests for passing in a string instead of a Path
    # Should give an assertion/typeError
