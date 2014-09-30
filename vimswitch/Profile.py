class Profile:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getDirName(self):
        return self.name.replace('/', '.')

    def __eq__(self, other):
        return isinstance(other, Profile) and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Profile('%s')" % self.name
