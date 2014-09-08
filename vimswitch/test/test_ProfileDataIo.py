import unittest
import Stubs
import os
from TestHelpers import assertNoCall
from vimswitch.ProfileDataIo import ProfileDataIo


class TestProfileDataIo(unittest.TestCase):
    def setUp(self):
        self.diskIo = Stubs.DiskIoStub()
        self.settings = Stubs.SettingsStub()
        self.profileDataIo = ProfileDataIo(self.settings, self.diskIo)

    # ProfileDataIo.delete#files

    def test_delete_whenFileExists_deletesFile(self):
        profilePath = os.path.normpath('/home/foo')
        self.diskIo.fileExists.return_value = True

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteFile.assert_any_call(os.path.normpath('/home/foo/.vimrc'))

    def test_delete_whenFileDoesNotExists_doesNotDeleteFile(self):
        profilePath = os.path.normpath('/home/foo')
        self.diskIo.fileExists.return_value = False

        self.profileDataIo.delete(profilePath)

        assertNoCall(self.diskIo.deleteFile, os.path.normpath('/home/foo/.vimrc'))

    def test_delete_usesGetProfileFiles_fromSettings(self):
        profilePath = os.path.normpath('/home/foo')
        self.diskIo.fileExists.return_value = True
        self.settings.profileFiles = ['testProfileFile']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteFile.assert_any_call(os.path.normpath('/home/foo/testProfileFile'))

    def test_delete_deletesMultipleFiles(self):
        profilePath = os.path.normpath('/home/foo')
        self.diskIo.fileExists.return_value = True
        self.settings.profileFiles = ['file1', 'file2']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteFile.assert_any_call(os.path.normpath('/home/foo/file1'))
        self.diskIo.deleteFile.assert_any_call(os.path.normpath('/home/foo/file2'))

    # ProfileDataIo.delete#dirs

    def test_delete_whenDirExists_deletesDir(self):
        profilePath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = True

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteDir.assert_any_call(os.path.normpath('/home/foo/.vim'))

    def test_delete_whenDirDoesNotExists_doesNotDeleteDir(self):
        profilePath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = False

        self.profileDataIo.delete(profilePath)

        assertNoCall(self.diskIo.deleteDir, os.path.normpath('/home/foo/.vim'))

    def test_delete_usesGetProfileDirs_fromSettings(self):
        profilePath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.profileDirs = ['testProfileDir']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteDir.assert_any_call(os.path.normpath('/home/foo/testProfileDir'))

    def test_delete_deletesMultipleDirs(self):
        profilePath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.profileDirs = ['dir1', 'dir2']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteDir.assert_any_call(os.path.normpath('/home/foo/dir1'))
        self.diskIo.deleteDir.assert_any_call(os.path.normpath('/home/foo/dir2'))

    def test_delete_deletesFilesAndDirs(self):
        profilePath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.profileFiles = ['file1', 'file2']
        self.settings.profileDirs = ['dir1', 'dir2']

        self.profileDataIo.delete(profilePath)

        self.diskIo.deleteFile.assert_any_call(os.path.normpath('/home/foo/file1'))
        self.diskIo.deleteFile.assert_any_call(os.path.normpath('/home/foo/file2'))
        self.diskIo.deleteDir.assert_any_call(os.path.normpath('/home/foo/dir1'))
        self.diskIo.deleteDir.assert_any_call(os.path.normpath('/home/foo/dir2'))

    # ProfileDataIo.copy#files

    def test_copy_whenFileExists_copiesFile(self):
        srcPath = os.path.normpath('/home/foo/.vimswitch/test.vimrc')
        destPath = os.path.normpath('/home/foo')
        self.diskIo.fileExists.return_value = True

        self.profileDataIo.copy(srcPath, destPath)

        srcFile = os.path.normpath('/home/foo/.vimswitch/test.vimrc/.vimrc')
        destFile = os.path.normpath('/home/foo/.vimrc')
        self.diskIo.copyFile.assert_any_call(srcFile, destFile)

    def test_copy_whenFileDoesNotExists_doesNotCopyFile(self):
        srcPath = os.path.normpath('/home/foo/.vimswitch/test.vimrc')
        destPath = os.path.normpath('/home/foo')
        self.diskIo.fileExists.return_value = False

        self.profileDataIo.copy(srcPath, destPath)

        srcFile = os.path.normpath('/home/foo/.vimswitch/test.vimrc/.vimrc')
        destFile = os.path.normpath('/home/foo/.vimrc')
        assertNoCall(self.diskIo.copyFile, srcFile, destFile)

    def test_copy_usesGetProfileFiles_fromSettings(self):
        srcPath = os.path.normpath('/home/foo/.vimswitch/test.vimrc')
        destPath = os.path.normpath('/home/foo')
        self.diskIo.fileExists.return_value = True
        self.settings.profileFiles = ['testProfileFile']

        self.profileDataIo.copy(srcPath, destPath)

        srcFile = os.path.normpath('/home/foo/.vimswitch/test.vimrc/testProfileFile')
        destFile = os.path.normpath('/home/foo/testProfileFile')
        self.diskIo.copyFile.assert_any_call(srcFile, destFile)

    def test_copy_copiesMultipleFiles(self):
        srcPath = os.path.normpath('/home/foo/.vimswitch/test.vimrc')
        destPath = os.path.normpath('/home/foo')
        self.diskIo.fileExists.return_value = True
        self.settings.profileFiles = ['file1', 'file2']

        self.profileDataIo.copy(srcPath, destPath)

        srcFile1 = os.path.normpath('/home/foo/.vimswitch/test.vimrc/file1')
        destFile1 = os.path.normpath('/home/foo/file1')
        srcFile2 = os.path.normpath('/home/foo/.vimswitch/test.vimrc/file2')
        destFile2 = os.path.normpath('/home/foo/file2')
        self.diskIo.copyFile.assert_any_call(srcFile1, destFile1)
        self.diskIo.copyFile.assert_any_call(srcFile2, destFile2)

    # ProfileDataIo.copy#dirs

    def test_copy_whenDirExists_copiesDir(self):
        srcPath = os.path.normpath('/home/foo/.vimswitch/test.vimrc')
        destPath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = True

        self.profileDataIo.copy(srcPath, destPath)

        srcDir = os.path.normpath('/home/foo/.vimswitch/test.vimrc/.vim')
        destDir = os.path.normpath('/home/foo/.vim')
        self.diskIo.copyDir.assert_any_call(srcDir, destDir)

    def test_copy_whenDirDoesNotExists_doesNotCopyDir(self):
        srcPath = os.path.normpath('/home/foo/.vimswitch/test.vimrc')
        destPath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = False

        self.profileDataIo.copy(srcPath, destPath)

        srcDir = os.path.normpath('/home/foo/.vimswitch/test.vimrc/.vim')
        destDir = os.path.normpath('/home/foo/.vim')
        assertNoCall(self.diskIo.copyDir, srcDir, destDir)

    def test_copy_usesGetProfileDirs_fromSettings(self):
        srcPath = os.path.normpath('/home/foo/.vimswitch/test.vimrc')
        destPath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.profileDirs = ['testProfileDir']

        self.profileDataIo.copy(srcPath, destPath)

        srcDir = os.path.normpath('/home/foo/.vimswitch/test.vimrc/testProfileDir')
        destDir = os.path.normpath('/home/foo/testProfileDir')
        self.diskIo.copyDir.assert_any_call(srcDir, destDir)

    def test_copy_copiesMultipleDirs(self):
        srcPath = os.path.normpath('/home/foo/.vimswitch/test.vimrc')
        destPath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.profileDirs = ['dir1', 'dir2']

        self.profileDataIo.copy(srcPath, destPath)

        srcDir1 = os.path.normpath('/home/foo/.vimswitch/test.vimrc/dir1')
        destDir1 = os.path.normpath('/home/foo/dir1')
        srcDir2 = os.path.normpath('/home/foo/.vimswitch/test.vimrc/dir2')
        destDir2 = os.path.normpath('/home/foo/dir2')
        self.diskIo.copyDir.assert_any_call(srcDir1, destDir1)
        self.diskIo.copyDir.assert_any_call(srcDir2, destDir2)

    def test_copy_copiesFilesAndDirs(self):
        srcPath = os.path.normpath('/home/foo/.vimswitch/test.vimrc')
        destPath = os.path.normpath('/home/foo')
        self.diskIo.dirExists.return_value = True
        self.settings.profileFiles = ['file1', 'file2']
        self.settings.profileDirs = ['dir1', 'dir2']

        self.profileDataIo.copy(srcPath, destPath)

        srcFile1 = os.path.normpath('/home/foo/.vimswitch/test.vimrc/file1')
        destFile1 = os.path.normpath('/home/foo/file1')
        srcFile2 = os.path.normpath('/home/foo/.vimswitch/test.vimrc/file2')
        destFile2 = os.path.normpath('/home/foo/file2')
        srcDir1 = os.path.normpath('/home/foo/.vimswitch/test.vimrc/dir1')
        destDir1 = os.path.normpath('/home/foo/dir1')
        srcDir2 = os.path.normpath('/home/foo/.vimswitch/test.vimrc/dir2')
        destDir2 = os.path.normpath('/home/foo/dir2')
        self.diskIo.copyFile.assert_any_call(srcFile1, destFile1)
        self.diskIo.copyFile.assert_any_call(srcFile2, destFile2)
        self.diskIo.copyDir.assert_any_call(srcDir1, destDir1)
        self.diskIo.copyDir.assert_any_call(srcDir2, destDir2)

    # TODO: Add tests for passing in a string instead of a Path
    # Should give an assertion/typeError
