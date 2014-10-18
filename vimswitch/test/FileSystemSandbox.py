import os
import shutil
import vimswitch.six.moves.builtins as builtins


class FileSystemSandbox:
    """
    This static class sets up a global sandbox where all disk modification is
    disabled except inside the sandbox directory. If an operation outside the
    sandbox directory occurs, a FileSystemSandboxError is thrown.

    Read-only disk operations will still be allowed outside the sandbox
    directory, however.
    """

    enabled = False
    sandboxRoot = ''

    @classmethod
    def enable(self, sandboxRoot):
        if self.enabled:
            raise RuntimeError('Sandbox already enabled')

        self.enabled = True
        self.sandboxRoot = sandboxRoot
        self._setUpSafeOperations()

    @classmethod
    def disable(self):
        if not self.enabled:
            raise RuntimeError('Sandbox already disabled')

        self.enabled = False
        self._tearDownSafeOperations()

    @classmethod
    def _setUpSafeOperations(self):
        self._real_builtin_open = builtins.open
        self._real_os_mkdir = os.mkdir
        self._real_os_makedirs = os.makedirs
        self._real_os_remove = os.remove
        self._real_os_path_isfile = os.path.isfile
        self._real_os_path_isdir = os.path.isdir
        self._real_shutil_copy = shutil.copy
        self._real_shutil_move = shutil.move
        self._real_shutil_copytree = shutil.copytree
        self._real_shutil_rmtree = shutil.rmtree

        builtins.open = self._safe_builtin_open
        os.mkdir = self._safe_os_mkdir
        os.makedirs = self._safe_os_makedirs
        os.remove = self._safe_os_remove
        shutil.copy = self._safe_shutil_copy
        shutil.move = self._safe_shutil_move
        shutil.copytree = self._safe_shutil_copytree
        shutil.rmtree = self._safe_shutil_rmtree

    @classmethod
    def _tearDownSafeOperations(self):
        builtins.open = self._real_builtin_open
        os.mkdir = self._real_os_mkdir
        os.makedirs = self._real_os_makedirs
        os.remove = self._real_os_remove
        shutil.copy = self._real_shutil_copy
        shutil.move = self._real_shutil_move
        shutil.copytree = self._real_shutil_copytree
        shutil.rmtree = self._real_shutil_rmtree

    @classmethod
    def _safe_builtin_open(self, path, mode='r', *args, **kwargs):
        # We only verify if the file is being opened for writing or appending.
        # Read only access should be allowed.
        if mode.find('w') != -1 or mode.find('a') != -1:
            self._verifyPath(path)
        return self._real_builtin_open(path, mode, *args, **kwargs)

    @classmethod
    def _safe_os_mkdir(self, path, *args, **kwargs):
        self._verifyPath(path)
        self._real_os_mkdir(path, *args, **kwargs)

    @classmethod
    def _safe_os_makedirs(self, path, *args, **kwargs):
        self._verifyPath(path)
        self._real_os_makedirs(path, *args, **kwargs)

    @classmethod
    def _safe_os_remove(self, path):
        self._verifyPath(path)
        self._real_os_remove(path)

    @classmethod
    def _safe_shutil_copy(self, src, dst):
        # Only need to verify destination path since src will not be modified
        self._verifyPath(dst)
        self._real_shutil_copy(src, dst)

    @classmethod
    def _safe_shutil_move(self, src, dst):
        self._verifyPath(src)
        self._verifyPath(dst)
        self._real_shutil_move(src, dst)

    @classmethod
    def _safe_shutil_copytree(self, src, dst, *args, **kwargs):
        # Only need to verify destination path since src will not be modified
        self._verifyPath(dst)
        self._real_shutil_copytree(src, dst, *args, **kwargs)

    @classmethod
    def _safe_shutil_rmtree(self, path, *args, **kwargs):
        self._verifyPath(path)
        self._real_shutil_rmtree(path, *args, **kwargs)

    @classmethod
    def _verifyPath(self, path):
        "Checks that path is inside the sandbox"
        absPath = os.path.abspath(path)
        if not absPath.startswith(self.sandboxRoot):
            raise FileSystemSandboxError(path)


class FileSystemSandboxError(Exception):
    def __init__(self, path):
        Exception.__init__(self, 'Tried to access path outside sandbox: %s' % path)
