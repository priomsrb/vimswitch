import os
from zipfile import ZipFile
from .ProfileUrlResolver import getProfileUrl
from .Settings import getSettings
from .FileDownloader import getFileDownloader
from .ProfileCache import getProfileCache
from .DiskIo import getDiskIo


class ProfileRetriever:
    def __init__(self, settings, fileDownloader, profileCache, diskIo):
        self.settings = settings
        self.fileDownloader = fileDownloader
        self.profileCache = profileCache
        self.diskIo = diskIo

    def retrieve(self, profile):
        url = getProfileUrl(profile)
        print('Downloading profile from %s' % url)
        downloadsPath = self.settings.downloadsPath
        downloadedFilePath = self.fileDownloader.download(url, downloadsPath)
        extractionDir = os.path.splitext(downloadedFilePath)[0]
        ZipFile(downloadedFilePath).extractall(extractionDir)

        if self.profileCache.contains(profile):
            self.profileCache.delete(profile)

        profileDir = self.profileCache.getProfileLocation(profile)
        self.diskIo.move(extractionDir, profileDir)


def getProfileRetriever(app):
    return app.get('profileRetriever', createProfileRetriever(app))


def createProfileRetriever(app):
    settings = getSettings(app)
    fileDownloader = getFileDownloader(app)
    profileCache = getProfileCache(app)
    diskIo = getDiskIo(app)
    profileRetriever = ProfileRetriever(settings, fileDownloader, profileCache, diskIo)
    return profileRetriever
