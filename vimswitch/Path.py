import os


class Path:
    def __init__(self, pathString):
        self.pathString = os.path.normpath(pathString)

    def join(self, path):
        if isString(path):
            joinedPathStr = os.path.join(self.pathString, path)
            joinedPath = Path(joinedPathStr)
        elif isinstance(path, Path):
            joinedPathStr = os.path.join(self.pathString, path.pathString)
            joinedPath = Path(joinedPathStr)
        return joinedPath

    def __eq__(self, other):
        if isString(other):
            return other == self.pathString
        elif isinstance(other, Path):
            return self.pathString == other.pathString

    def __ne__(self, other):
        return not self.__eq__(other)

    def __unicode__(self):
        return self.pathString

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return unicode(self).encode('utf-8')


def isString(x):
    return isinstance(x, str) or isinstance(x, basestring)
