import unittest
import sys
from vimswitch.Path import Path


class PathTest(unittest.TestCase):
    def test_init_simple(self):
        path = Path('test')
        self.assertEqual(path, 'test')

    def test_init_withSlashes(self):
        path = Path('dir/file.txt')
        if self.isWindows():
            self.assertEqual(path, 'dir\\file.txt')
        else:
            self.assertEqual(path, 'dir/file.txt')

    def test_joinPath(self):
        path1 = Path('/home/foo')
        path2 = Path('bar')

        joinedPath = path1.join(path2)

        if self.isWindows():
            expectedPath = Path('\\home\\foo\\bar')
            self.assertEqual(joinedPath, expectedPath)
        else:
            expectedPath = Path('/home/foo/bar')
            self.assertEqual(joinedPath, expectedPath)

    def test_joinStr(self):
        path1 = Path('/home/foo')
        path2 = 'bar'

        joinedPath = path1.join(path2)

        if self.isWindows():
            expectedPath = Path('\\home\\foo\\bar')
            self.assertEqual(joinedPath, expectedPath)
        else:
            expectedPath = Path('/home/foo/bar')
            self.assertEqual(joinedPath, expectedPath)

    def test_joinPath_keepsOriginal(self):
        path1 = Path('/home/foo')
        path2 = Path('bar')

        path1.join(path2)

        self.assertEqual(path1, Path('/home/foo'))

    def test_joinStr_keepsOriginal(self):
        path1 = Path('/home/foo')
        path2 = 'bar'

        path1.join(path2)

        self.assertEqual(path1, Path('/home/foo'))

    def test_equal(self):
        path1 = Path('foo/bar')
        path2 = Path('foo/bar')

        self.assertEqual(path1, path2)

    def test_notEqual(self):
        path1 = Path('foo/bar1')
        path2 = Path('foo/bar2')

        self.assertNotEqual(path1, path2)

    # Helpers

    def isWindows(self):
        return 'win' in sys.platform
