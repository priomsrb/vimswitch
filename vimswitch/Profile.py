class Profile:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getDirName(self):
        return self.name.replace('/', '.')
