class Profile:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getDirName(self):
        return self.name.replace('/', '.')

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return "Profile('%s')" % self.name
