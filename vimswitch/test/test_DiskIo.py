from .FileSystemTestCase import FileSystemTestCase
from vimswitch.DiskIo import DiskIo


class TestDiskIo(FileSystemTestCase):
    def setUp(self):
        FileSystemTestCase.setUp(self)
        self.diskIo = DiskIo()

    # DiskIo.createFile

    def test_createFile_hasCorrectContent(self):
        filePath = self.getTestPath('file1.txt')
        #filePath = 'file1.txt'

        self.diskIo.createFile(filePath, 'test data')

        actual = self.diskIo.getFileContents(filePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_createFile_withParentDir_hasCorrectContent(self):
        dirPath = self.getTestPath('dir1')
        filePath = self.getTestPath('dir1/file1.txt')
        self.diskIo.createDir(dirPath)

        self.diskIo.createFile(filePath, 'test data')

        actual = self.diskIo.getFileContents(filePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_createFile_nonExistantParentDir_raisesError(self):
        filePath = self.getTestPath('non_existant/file1.txt')

        self.assertRaises(IOError, self.diskIo.createFile, filePath, 'test data')

    # DiskIo.getFileContents

    def test_getFileContents_returnsCorrectContent(self):
        filePath = self.getTestPath('file1.txt')
        self.diskIo.createFile(filePath, 'test data')

        actual = self.diskIo.getFileContents(filePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_getFileContents_nonExistantFile_raisesError(self):
        filePath = self.getTestPath('file1.txt')

        self.assertRaises(IOError, self.diskIo.getFileContents, filePath)

    def test_getFileContents_onDir_raisesError(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDir(dirPath)

        self.assertRaises(IOError, self.diskIo.getFileContents, dirPath)

    # DiskIo.copyFile

    def test_copyFile_copiesFile(self):
        filePath = self.getTestPath('file1.txt')
        copiedFilePath = self.getTestPath('copied_file1.txt')
        self.diskIo.createFile(filePath, 'test data')

        self.diskIo.copyFile(filePath, copiedFilePath)

        actual = self.diskIo.getFileContents(copiedFilePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_copyFile_copiesIntoDir(self):
        filePath = self.getTestPath('file1.txt')
        dirPath = self.getTestPath('dir1')
        copiedFilePath = self.getTestPath('dir1/file1.txt')
        self.diskIo.createFile(filePath, 'test data')
        self.diskIo.createDir(dirPath)

        self.diskIo.copyFile(filePath, dirPath)

        actual = self.diskIo.getFileContents(copiedFilePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_copyFile_overwritesExisting(self):
        filePath = self.getTestPath('file1.txt')
        existingFilePath = self.getTestPath('existing_file1.txt')
        self.diskIo.createFile(filePath, 'test data')
        self.diskIo.createFile(existingFilePath, 'existing data')

        self.diskIo.copyFile(filePath, existingFilePath)

        actual = self.diskIo.getFileContents(existingFilePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_copyFile_sourceFileDoesNotExist_raisesError(self):
        filePath = self.getTestPath('file1.txt')
        copiedFilePath = self.getTestPath('copied_file1.txt')

        self.assertRaises(IOError, self.diskIo.copyFile, filePath, copiedFilePath)

    # DiskIo.move

    def test_move_movesFile(self):
        filePath = self.getTestPath('file1.txt')
        movedFilePath = self.getTestPath('moved_file1.txt')
        self.diskIo.createFile(filePath, 'test data')

        self.diskIo.move(filePath, movedFilePath)

        self.assertFalse(self.diskIo.anyExists(filePath))
        actual = self.diskIo.getFileContents(movedFilePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_move_overwritesExisting(self):
        filePath = self.getTestPath('file1.txt')
        existingFilePath = self.getTestPath('existing.txt')
        self.diskIo.createFile(filePath, 'test data')
        self.diskIo.createFile(existingFilePath, 'existing data')

        self.diskIo.move(filePath, existingFilePath)

        self.assertFalse(self.diskIo.anyExists(filePath))
        actual = self.diskIo.getFileContents(existingFilePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_move_movesIntoExistingDir(self):
        filePath = self.getTestPath('file1.txt')
        existingDir = self.getTestPath('existing')
        movedFilePath = self.getTestPath('existing/file1.txt')
        self.diskIo.createFile(filePath, 'test data')
        self.diskIo.createDir(existingDir)

        self.diskIo.move(filePath, movedFilePath)

        self.assertFalse(self.diskIo.anyExists(filePath))
        actual = self.diskIo.getFileContents(movedFilePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    def test_move_intoNonExistingDir_raisesError(self):
        filePath = self.getTestPath('file1.txt')
        movedFilePath = self.getTestPath('non_existing/file1.txt')
        self.diskIo.createFile(filePath, 'test data')

        self.assertRaises(IOError, self.diskIo.move, filePath, movedFilePath)

    def test_move_intoItself_doesNothing(self):
        filePath = self.getTestPath('file1.txt')
        self.diskIo.createFile(filePath, 'test data')

        self.diskIo.move(filePath, filePath)
        actual = self.diskIo.getFileContents(filePath)
        expected = 'test data'
        self.assertEqual(actual, expected)

    # DiskIo.deleteFile

    def test_deleteFile_deletesFile(self):
        filePath = self.getTestPath('file1.txt')
        self.diskIo.createFile(filePath, 'test data')

        self.diskIo.deleteFile(filePath)

        self.assertFalse(self.diskIo.anyExists(filePath))

    def test_deleteFile_fileDoesNotExist_raisesError(self):
        filePath = self.getTestPath('file1.txt')
        self.assertRaises(OSError, self.diskIo.deleteFile, filePath)

    def test_deleteFile_fileIsDir_raisesError(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDir(dirPath)
        self.assertRaises(OSError, self.diskIo.deleteFile, dirPath)

    # DiskIo.fileExists

    def test_fileExists_fileDoesExist_returnsTrue(self):
        filePath = self.getTestPath('file1.txt')
        self.diskIo.createFile(filePath, 'test data')

        self.assertTrue(self.diskIo.fileExists(filePath))

    def test_fileExists_fileDoesNotExist_returnsFalse(self):
        filePath = self.getTestPath('file1.txt')
        self.assertFalse(self.diskIo.fileExists(filePath))

    def test_fileExists_dirExists_returnsFalse(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDir(dirPath)
        self.assertFalse(self.diskIo.fileExists(dirPath))

    # DiskIo.createDir

    def test_createDir_createsDir(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDir(dirPath)
        self.assertTrue(self.diskIo.dirExists(dirPath))

    def test_createDir_withParent_createsDir(self):
        parentDirPath = self.getTestPath('parent')
        childDirPath = self.getTestPath('parent/child')

        self.diskIo.createDir(parentDirPath)
        self.diskIo.createDir(childDirPath)

        self.assertTrue(self.diskIo.dirExists(childDirPath))

    def test_createDir_withoutParent_raisesError(self):
        childDirPath = self.getTestPath('parent/child')
        self.assertRaises(OSError, self.diskIo.createDir, childDirPath)

    def test_createDir_dirAlreadyExists_raisesError(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDir(dirPath)
        self.assertRaises(OSError, self.diskIo.createDir, dirPath)

    # DiskIo.createDirWithParents

    def test_createDirWithParents_createsDir(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDirWithParents(dirPath)
        self.assertTrue(self.diskIo.dirExists(dirPath))

    def test_createDirWithParents_withParent_createsDir(self):
        parentDirPath = self.getTestPath('parent')
        childDirPath = self.getTestPath('parent/child')

        self.diskIo.createDirWithParents(parentDirPath)
        self.diskIo.createDirWithParents(childDirPath)

        self.assertTrue(self.diskIo.dirExists(childDirPath))

    def test_createDirWithParents_withoutParent_createsDir(self):
        childDirPath = self.getTestPath('parent/child')
        self.diskIo.createDirWithParents(childDirPath)
        self.assertTrue(self.diskIo.dirExists(childDirPath))

    def test_createDirWithParents_dirAlreadyExists_raisesError(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDirWithParents(dirPath)
        self.assertRaises(OSError, self.diskIo.createDirWithParents, dirPath)

    # DiskIo.copyDir

    def test_copyDir_copiesEmptyDir(self):
        dirPath = self.getTestPath('dir1')
        copiedDirPath = self.getTestPath('copiedDir')
        self.diskIo.createDir(dirPath)

        self.diskIo.copyDir(dirPath, copiedDirPath)

        self.assertTrue(self.diskIo.dirExists(copiedDirPath))

    def test_copyDir_copiesRecursively(self):
        dirPath = self.getTestPath('dir1')
        innerDirPath = self.getTestPath('dir1/innerDir')
        innerFilePath = self.getTestPath('dir1/innerFile.txt')
        copiedDirPath = self.getTestPath('copiedDir')
        copiedInnerDirPath = self.getTestPath('copiedDir/innerDir')
        copiedInnerFilePath = self.getTestPath('copiedDir/innerFile.txt')
        self.diskIo.createDir(dirPath)
        self.diskIo.createDir(innerDirPath)
        self.diskIo.createFile(innerFilePath, 'test data')

        self.diskIo.copyDir(dirPath, copiedDirPath)

        self.assertTrue(self.diskIo.dirExists(copiedDirPath))
        self.assertTrue(self.diskIo.dirExists(copiedInnerDirPath))
        self.assertTrue(self.diskIo.fileExists(copiedInnerFilePath))
        self.assertEqual(self.diskIo.getFileContents(copiedInnerFilePath), 'test data')

    def test_copyDir_destParentDirDoesNotExist_createsParentDir(self):
        dirPath = self.getTestPath('dir1')
        copiedParentDirPath = self.getTestPath('non_existant')
        copiedDirPath = self.getTestPath('non_existant/copiedDir')
        self.diskIo.createDir(dirPath)

        self.diskIo.copyDir(dirPath, copiedDirPath)

        self.assertTrue(self.diskIo.dirExists(copiedParentDirPath))
        self.assertTrue(self.diskIo.dirExists(copiedDirPath))

    def test_copyDir_destDirExists_raisesError(self):
        dirPath = self.getTestPath('dir1')
        existingDirPath = self.getTestPath('existing')
        self.diskIo.createDir(dirPath)
        self.diskIo.createDir(existingDirPath)

        self.assertRaises(OSError, self.diskIo.copyDir, dirPath, existingDirPath)

    def test_copyDir_sourceDirDoesNotExist_raisesError(self):
        nonExistantDirPath = self.getTestPath('non_existant')
        copiedDirPath = self.getTestPath('copiedDir')
        self.assertRaises(OSError, self.diskIo.copyDir, nonExistantDirPath, copiedDirPath)

    # DiskIo.deleteDir

    def test_deleteDir_deletesEmptyDir(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDir(dirPath)

        self.diskIo.deleteDir(dirPath)

        self.assertFalse(self.diskIo.anyExists(dirPath))

    def test_deleteDir_dirContainsFiles_deletesDirAndContents(self):
        dirPath = self.getTestPath('dir1')
        innerDirPath = self.getTestPath('dir1/innerDir')
        innerFilePath = self.getTestPath('dir1/innerFile.txt')
        self.diskIo.createDir(dirPath)
        self.diskIo.createDir(innerDirPath)
        self.diskIo.createFile(innerFilePath, 'test data')

        self.diskIo.deleteDir(dirPath)

        self.assertFalse(self.diskIo.anyExists(dirPath))
        self.assertFalse(self.diskIo.anyExists(innerDirPath))
        self.assertFalse(self.diskIo.anyExists(innerFilePath))

    def test_deleteDir_dirDoesNotExist_raiseError(self):
        dirPath = self.getTestPath('dir1')
        self.assertRaises(OSError, self.diskIo.deleteDir, dirPath)

    def test_deleteDir_dirIsFile_raiseError(self):
        filePath = self.getTestPath('file1.txt')
        self.diskIo.createFile(filePath, 'test data')
        self.assertRaises(OSError, self.diskIo.deleteDir, filePath)

    # DiskIo.dirExists

    def test_dirExists_dirDoesExist_returnsTrue(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDir(dirPath)
        self.assertTrue(self.diskIo.dirExists(dirPath))

    def test_dirExists_dirDoesNotExists_returnsFalse(self):
        dirPath = self.getTestPath('dir1')
        self.assertFalse(self.diskIo.dirExists(dirPath))

    def test_dirExists_fileExists_returnFalse(self):
        filePath = self.getTestPath('file1.txt')
        self.diskIo.createFile(filePath, 'test data')
        self.assertFalse(self.diskIo.dirExists(filePath))

    def test_dirExists_parentDirDoesNotExist_returnsFalse(self):
        childDir = self.getTestPath('parentDir/childDir')
        self.assertFalse(self.diskIo.dirExists(childDir))

    # DiskIo.isDirEmpty

    def test_isDirEmpty_emptyDir_returnsTrue(self):
        dirPath = self.getTestPath('empty')
        self.diskIo.createDir(dirPath)

        self.assertTrue(self.diskIo.isDirEmpty(dirPath))

    def test_isDirEmpty_nonEmptyDir_returnsFalse(self):
        dirPath = self.getTestPath('non_empty')
        filePath = self.getTestPath('non_empty/file1.txt')
        self.diskIo.createDir(dirPath)
        self.diskIo.createFile(filePath, 'test data')

        self.assertFalse(self.diskIo.isDirEmpty(dirPath))

    def test_isDirEmpty_nonExistantDir_raisesError(self):
        dirPath = self.getTestPath('non_existant')

        self.assertRaises(OSError, self.diskIo.isDirEmpty, dirPath)

    def test_isDirEmpty_onFile_raisesError(self):
        filePath = self.getTestPath('file1.txt')
        self.diskIo.createFile(filePath, 'test data')

        self.assertRaises(OSError, self.diskIo.isDirEmpty, filePath)

    # DiskIo.anyExists

    def test_anyExists_withFile_returnsTrue(self):
        filePath = self.getTestPath('file1.txt')
        self.diskIo.createFile(filePath, 'test data')
        self.assertTrue(self.diskIo.anyExists(filePath))

    def test_anyExists_withDir_returnsTrue(self):
        dirPath = self.getTestPath('dir1')
        self.diskIo.createDir(dirPath)
        self.assertTrue(self.diskIo.anyExists(dirPath))

    def test_anyExists_withNothing_returnsFalse(self):
        nonExistantPath = self.getTestPath('non_existant')
        self.assertFalse(self.diskIo.anyExists(nonExistantPath))
