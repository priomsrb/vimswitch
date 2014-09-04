import os
from IntegrationTestCase import IntegrationTestCase
from vimswitch.DiskIo import DiskIo


class TestDiskIo(IntegrationTestCase):
    def setUp(self):
        self.clearWorkingDirectory()
        self.diskIo = DiskIo()

    def tearDown(self):
        self.clearWorkingDirectory()

    # DiskIo.copyFile

    def test_copyFile_copiesFile(self):
        filePath = self.getFullPath('file1.txt')
        copiedFilePath = self.getFullPath('copied_file1.txt')
        self.createFile(filePath, 'test data')

        self.diskIo.copyFile(filePath, copiedFilePath)

        actual = self.getFileContents(copiedFilePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_copyFile_overwritesExisting(self):
        filePath = self.getFullPath('file1.txt')
        existingFilePath = self.getFullPath('existing_file1.txt')
        self.createFile(filePath, 'test data')
        self.createFile(existingFilePath, 'existing data')

        self.diskIo.copyFile(filePath, existingFilePath)

        actual = self.getFileContents(existingFilePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_copyFile_sourceFileDoesNotExist_raisesError(self):
        filePath = self.getFullPath('file1.txt')
        copiedFilePath = self.getFullPath('copied_file1.txt')

        self.assertRaises(IOError, self.diskIo.copyFile, filePath, copiedFilePath)

    # DiskIo.deleteFile

    def test_deleteFile_deletesFile(self):
        filePath = self.getFullPath('file1.txt')
        self.createFile(filePath, 'test data')

        self.diskIo.deleteFile(filePath)

        self.assertFalse(os.path.exists(filePath))

    def test_deleteFile_fileDoesNotExist_raisesError(self):
        filePath = self.getFullPath('file1.txt')
        self.assertRaises(OSError, self.diskIo.deleteFile, filePath)

    def test_deleteFile_fileIsDir_raisesError(self):
        dirPath = self.getFullPath('dir1')
        self.createDir(dirPath)
        self.assertRaises(OSError, self.diskIo.deleteFile, dirPath)

    # DiskIo.fileExists

    def test_fileExists_fileDoesExist_returnsTrue(self):
        filePath = self.getFullPath('file1.txt')
        self.createFile(filePath, 'test data')

        self.assertTrue(self.diskIo.fileExists(filePath))

    def test_fileExists_fileDoesNotExist_returnsFalse(self):
        filePath = self.getFullPath('file1.txt')
        self.assertFalse(self.diskIo.fileExists(filePath))

    def test_fileExists_dirExists_returnsFalse(self):
        dirPath = self.getFullPath('dir1')
        self.createDir(dirPath)
        self.assertFalse(self.diskIo.fileExists(dirPath))

    # DiskIo.createDir

    def test_createDir_createsDir(self):
        dirPath = self.getFullPath('dir1')
        self.diskIo.createDir(dirPath)
        self.assertTrue(os.path.isdir(dirPath))

    def test_createDir_withParent_createsDir(self):
        parentDirPath = self.getFullPath('parent')
        childDirPath = self.getFullPath('parent/child')

        self.diskIo.createDir(parentDirPath)
        self.diskIo.createDir(childDirPath)

        self.assertTrue(os.path.isdir(childDirPath))

    def test_createDir_withoutParent_raisesError(self):
        childDirPath = self.getFullPath('parent/child')
        self.assertRaises(OSError, self.diskIo.createDir, childDirPath)

    def test_createDir_dirAlreadyExists_raisesError(self):
        dirPath = self.getFullPath('dir1')
        self.diskIo.createDir(dirPath)
        self.assertRaises(OSError, self.diskIo.createDir, dirPath)

    # DiskIo.copyDir

    def test_copyDir_copiesEmptyDir(self):
        dirPath = self.getFullPath('dir1')
        copiedDirPath = self.getFullPath('copiedDir')
        self.createDir(dirPath)

        self.diskIo.copyDir(dirPath, copiedDirPath)

        self.assertTrue(os.path.isdir(copiedDirPath))

    def test_copyDir_copiesRecursively(self):
        dirPath = self.getFullPath('dir1')
        innerDirPath = self.getFullPath('dir1/innerDir')
        innerFilePath = self.getFullPath('dir1/innerFile.txt')
        copiedDirPath = self.getFullPath('copiedDir')
        copiedInnerDirPath = self.getFullPath('copiedDir/innerDir')
        copiedInnerFilePath = self.getFullPath('copiedDir/innerFile.txt')
        self.createDir(dirPath)
        self.createDir(innerDirPath)
        self.createFile(innerFilePath, 'test data')

        self.diskIo.copyDir(dirPath, copiedDirPath)

        self.assertTrue(os.path.isdir(copiedDirPath))
        self.assertTrue(os.path.isdir(copiedInnerDirPath))
        self.assertTrue(os.path.isfile(copiedInnerFilePath))
        self.assertEqual(self.getFileContents(copiedInnerFilePath), 'test data')

    def test_copyDir_destParentDirDoesNotExist_createsParentDir(self):
        dirPath = self.getFullPath('dir1')
        copiedParentDirPath = self.getFullPath('non_existant')
        copiedDirPath = self.getFullPath('non_existant/copiedDir')
        self.createDir(dirPath)

        self.diskIo.copyDir(dirPath, copiedDirPath)

        self.assertTrue(os.path.isdir(copiedParentDirPath))
        self.assertTrue(os.path.isdir(copiedDirPath))

    def test_copyDir_destDirExists_raisesError(self):
        dirPath = self.getFullPath('dir1')
        existingDirPath = self.getFullPath('existing')
        self.createDir(dirPath)
        self.createDir(existingDirPath)

        self.assertRaises(OSError, self.diskIo.copyDir, dirPath, existingDirPath)

    def test_copyDir_sourceDirDoesNotExist_raisesError(self):
        nonExistantDirPath = self.getFullPath('non_existant')
        copiedDirPath = self.getFullPath('copiedDir')
        self.assertRaises(OSError, self.diskIo.copyDir, nonExistantDirPath, copiedDirPath)

    # DiskIo.deleteDir

    def test_deleteDir_deletesEmptyDir(self):
        dirPath = self.getFullPath('dir1')
        self.createDir(dirPath)

        self.diskIo.deleteDir(dirPath)

        self.assertFalse(os.path.exists(dirPath))

    def test_deleteDir_dirContainsFiles_deletesDirAndContents(self):
        dirPath = self.getFullPath('dir1')
        innerDirPath = self.getFullPath('dir1/innerDir')
        innerFilePath = self.getFullPath('dir1/innerFile.txt')
        self.createDir(dirPath)
        self.createDir(innerDirPath)
        self.createFile(innerFilePath, 'test data')

        self.diskIo.deleteDir(dirPath)

        self.assertFalse(os.path.exists(dirPath))
        self.assertFalse(os.path.exists(innerDirPath))
        self.assertFalse(os.path.exists(innerFilePath))

    def test_deleteDir_dirDoesNotExist_raiseError(self):
        dirPath = self.getFullPath('dir1')
        self.assertRaises(OSError, self.diskIo.deleteDir, dirPath)

    def test_deleteDir_dirIsFile_raiseError(self):
        filePath = self.getFullPath('file1.txt')
        self.createFile(filePath, 'test data')
        self.assertRaises(OSError, self.diskIo.deleteDir, filePath)

    # DiskIo.dirExists

    def test_dirExists_dirDoesExist_returnsTrue(self):
        dirPath = self.getFullPath('dir1')
        self.createDir(dirPath)
        self.assertTrue(self.diskIo.dirExists(dirPath))

    def test_dirExists_dirDoesNotExists_returnsFalse(self):
        dirPath = self.getFullPath('dir1')
        self.assertFalse(self.diskIo.dirExists(dirPath))

    def test_dirExists_fileExists_returnFalse(self):
        filePath = self.getFullPath('file1.txt')
        self.createFile(filePath, 'test data')
        self.assertFalse(self.diskIo.dirExists(filePath))

    def test_dirExists_parentDirDoesNotExist_returnsFalse(self):
        childDir = self.getFullPath('parentDir/childDir')
        self.assertFalse(self.diskIo.dirExists(childDir))

    # Helper methods

    def createFile(self, filePath, contents):
        with open(filePath, 'w') as file:
            file.write(contents)

    def getFileContents(self, filePath):
        with open(filePath, 'r') as file:
            return file.read()

    def createDir(self, dirPath):
        os.mkdir(dirPath)
